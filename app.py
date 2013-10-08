from flask import Flask
from flask import request
from flask import redirect
import os
import json

from reddit_functions import RedditRetriever

app = Flask(__name__)
r = RedditRetriever()

@app.route('/', methods=['GET', 'POST'])
def initiate():
    r.cache_initial_data()
    return "Initiation complete!"

@app.route('/<int:pebble>/submissions', methods=['GET', 'POST'])
def submissions(pebble):
    return json.dumps(r.get_submission_dict(pebble))

@app.route('/<int:pebble>/comments/<int:id>', methods=['GET', 'POST'])
def comments(pebble, id):
        return json.dumps(r.get_comments_by_submission_id(pebble, id))

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    r.cache_initial_data()
    return "Reddit page updated!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port, debug=True)
