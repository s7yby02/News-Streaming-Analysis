from chat_downloader import ChatDownloader
import json


def scrap_chat_into_json(url: str, filename='chat') -> None:
    """
    Load data from a Youtube URL into a json file 
    """
    chat = ChatDownloader().get_chat(url)       # create a generator

    with open(f'{filename}.json','w') as file:
        json.dump([], file)
        print("chat.json file successfully created!")

    for index, message in enumerate(chat):      # iterate over messages
        with open(f'{filename}.json','r') as file:
            data = json.load(file)
            data.append(message)

        with open('chat.json','w') as file:
            json.dump(data, file, indent=2)
        print(f"{index} chat messages has been added to the json file")

def extract_chat_comment(object: dict) -> str:
    """
    extract and return the message from the message object
    """
    return object['message']

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=jfKfPfyJRdk'
    scrap_chat_into_json(url)