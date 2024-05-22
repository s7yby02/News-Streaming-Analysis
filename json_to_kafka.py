from kafka import KafkaProducer
import json, time
from chat_scraper import extract_chat_from_object


def json_to_kafka( topic: str, filepath='chat.json'):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    with open(filepath, 'r') as file:
        data = json.load(file)
    for dd in data:
        msg = extract_chat_from_object(dd)
        print(msg)
        producer.send(topic, value=msg.encode('utf-8'))
        time.sleep(1)

if __name__ == '__main__':
    json_to_kafka('chat')