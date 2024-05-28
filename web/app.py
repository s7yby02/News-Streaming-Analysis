from flask import Flask, request, jsonify, render_template
from threading import Thread
from flask_socketio import SocketIO, emit
from flask_funcs import scrape_captions, scrape_chat
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for SocketIO
# socketio = SocketIO(app)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/start_scraper', methods=['POST'])
def start_scraper():
    data = request.json
    # print(data)
    link = data.get('link')
    if not link:
        return jsonify({"error": "No link provided"}), 400
    
    # # Start chat scraping in a background thread
    # chat_thread = Thread(target=scrape_chat, args=(link,))
    # chat_thread.start()

    # # Start caption scraping in a background thread
    # caption_thread = Thread(target=scrape_captions, args=(link,))
    # caption_thread.start()

    # Start chat scraping in a background task
    socketio.start_background_task(scrape_chat, link)

    # Start caption scraping in a background task
    socketio.start_background_task(scrape_captions, link)


    return jsonify({"message": "Scraper started"}), 200

def send_sentiment_data(sentiment_data):
    socketio.emit('update_sentiment', sentiment_data)
    print("Data SENT INTO EVENT SOCKETTTTTTT")

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)
