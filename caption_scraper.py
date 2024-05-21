import time
from functions import *
from kafka import KafkaProducer

# Getting the chrome driver
driver = getDriver()

# Going to the link
link = "https://www.youtube.com/watch?v=gCNeDWCI0vo&ab_channel=AlJazeeraEnglish"
goToLink(link, driver)

playButton(driver)

# Finding the captions container
caption_container = getCaptionsContainer(driver)
print("Caption container Found!!")

# Kafka producer setup
producer = KafkaProducer(bootstrap_servers='localhost:9092')

last_text="."
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

                    producer.send('captions',value=text.encode('utf-8'))
                    last_text=text
                    

        time.sleep(1.5)
    except:
        print('No caption found')
