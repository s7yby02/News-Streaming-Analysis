from flask import Flask, request, jsonify, render_template
from threading import Thread
from flask_funcs import scrape_captions, scrape_chat

app = Flask(__name__)

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
    
    # Start chat scraping in a background thread
    chat_thread = Thread(target=scrape_chat, args=(link,))
    chat_thread.start()

    # Start caption scraping in a background thread
    caption_thread = Thread(target=scrape_captions, args=(link,))
    caption_thread.start()


    return jsonify({"message": "Scraper started"}), 200

if __name__ == '__main__':
    app.run(debug=True)
