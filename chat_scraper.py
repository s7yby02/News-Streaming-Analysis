from chat_downloader import ChatDownloader
import json, time
from functions import establish_mongodb_connection
# from typing import Tuple


def scrap_chat_into_json(url: str, filename='chat') -> None:
    """
    Load data from a Youtube URL into a json file 
    """
    chat = ChatDownloader().get_chat(url)       # create a generator

    with open(f'{filename}.json','w') as file:
        json.dump([], file)
        print("chat.json file successfully created!")

    for index, message in enumerate(chat):      # iterate over messages
        # print(type(message))
        with open(f'{filename}.json','r') as file:
            data = json.load(file)
            data.append(message)

        with open('chat.json','w') as file:
            json.dump(data, file, indent=2)
        print(f"{index + 1} chat messages has been added to the json file")
        break


def scrap_chat_into_mongodb(url: str, collection) -> None:
    chat = ChatDownloader().get_chat(url)

    for index, message in enumerate(chat):
        collection.insert_one(message)
        # time.sleep(1)
        print(f"{index + 1} chat documenet has been added to the database")


def extract_chat_from_object(object: dict) -> str:
    """
    extract and return the message from the message object
    """
    return object['message']

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=jfKfPfyJRdk'
    # scrap_chat_into_json(url)
    collection = establish_mongodb_connection('pfadb', 'chatCollection')
    scrap_chat_into_mongodb(url, collection)