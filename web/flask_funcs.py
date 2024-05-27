import time
from functions import getDriver, goToLink, playButton, getCaptionsContainer, getCaptionsLines
from kafka import KafkaProducer
from chat_downloader import ChatDownloader


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
                        print(text)
                        producer.send('captions', value=text.encode('utf-8'))
                        last_text = text

            time.sleep(1.5)
        except:
            print('No caption found')

def scrape_chat(url: str):
    chat = ChatDownloader().get_chat(url)

    for index, msg in enumerate(chat):
        print(msg)
        print(f"{index+1} chat messages read!!!!")
        if index > 3: break


