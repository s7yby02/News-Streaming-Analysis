import time
from functions import getDriver, goToLink, playButton, getCaptionsContainer, getCaptionsLines
from kafka import KafkaProducer
from chat_downloader import ChatDownloader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
from typing import Tuple

# Load NRC Emotion Lexicon
nrc = pd.read_csv('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', names=['word', 'emotion', 'association'], sep='\t')


def scrape_captions(link):
    # Getting the chrome driver
    driver = getDriver()

    # Going to the link
    goToLink(link, driver)

    playButton(driver)

    # Finding the captions container
    caption_container = getCaptionsContainer(driver)
    print("Caption container Found!!")

    # Kafka producer setup
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    last_text = "."
    while True:
        try:
            # Getting the existing lines from the captions
            caption_lines = getCaptionsLines(driver)

            if len(caption_lines):
                for line in caption_lines:
                    # Extract text from each segment within a line
                    text = line.text
                    if text != last_text:
                        # print(text)
                        producer.send('captions', value=text.encode('utf-8'))
                        last_text = text

            time.sleep(1.5)
        except:
            print('No caption found')

def scrape_chat(url: str):
    from app import send_sentiment_data
    

    chat = ChatDownloader().get_chat(url)
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    total_messages = 0

    for index, msg in enumerate(chat):
        message = msg['message']
        emotion, sentiment = detect_emotion_and_sentiment(message)
        total_messages += 1
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1

        # Calculate percentages
        sentiment_data = {
            'positive': (sentiment_counts['positive'] / total_messages) * 100,
            'negative': (sentiment_counts['negative'] / total_messages) * 100,
            'neutral': (sentiment_counts['neutral'] / total_messages) * 100
        }
        send_sentiment_data(sentiment_data)

    # for index, msg in enumerate(chat):
    #     # print(msg['message'])
    #     message = msg['message']
    #     emotion, sentiment = detect_emotion_and_sentiment(message)
    #     print(detect_emotion_and_sentiment(msg['message']))
    #     print(f"{index+1} chat messages read!!!!")
    #     if index > 30: break


def detect_emotion_and_sentiment(text: str)->Tuple[str, str]:
    """
    It returns the emotion of the text and the global sentiment.
    """
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]

    emotion_counter = Counter()
    sentiment_counter = Counter()
    for word in words:
        emotions = nrc[(nrc['word'] == word) & (nrc['association'] == 1) & (~nrc['emotion'].isin(['positive', 'negative']))]['emotion']
        sentiment = nrc[(nrc['word'] == word) & (nrc['association'] == 1) & (nrc['emotion'].isin(['positive', 'negative']))]['emotion']
        
        emotion_counter.update(emotions)
        sentiment_counter.update(sentiment)

    most_common_emotion = emotion_counter.most_common(1)[0][0] if emotion_counter else 'neutral'
    positive_sentiment_count = sentiment_counter.get('positive', 0)
    negative_sentiment_count = sentiment_counter.get('negative', 0)
    
    overall_sentiment = ('positive' if positive_sentiment_count > negative_sentiment_count else 'negative' 
                         if negative_sentiment_count > positive_sentiment_count else 'neutral')

    return most_common_emotion, overall_sentiment