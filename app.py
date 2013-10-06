from flask import Flask
from flask import request
from flask import redirect
import os
import json

from reddit_functions import get_submission_dict
from reddit_functions import get_comments_by_submission_id
from reddit_functions import build_dictionaries
from reddit_functions import cache_initial_data

app = Flask(__name__)

@app.route('/<int:pebble>/submissions', methods=['GET', 'POST'])
def submissions(pebble):
    return json.dumps(get_submission_dict(pebble))

@app.route('/<int:pebble>/comments/<int:id>', methods=['GET', 'POST'])
def comments(pebble, id):
        return json.dumps(get_comments_by_submission_id(pebble, id))

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    cache_initial_data()
    return "Reddit page updated!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port, debug=True)
