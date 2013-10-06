from flask import Flask
from flask import request
from flask import redirect
import os
import json

from reddit_functions import get_submission_dict
from reddit_functions import get_comments_by_submission_id
from reddit_functions import build_dictionaries

app = Flask(__name__)

@app.route('/submissions', methods=['GET', 'POST'])
def submissions():
    return json.dumps(get_submission_dict())

@app.route('/comments/<int:id>', methods=['GET', 'POST'])
def comments(id):
        return json.dumps(get_comments_by_submission_id(id))

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    build_dictionaries()
    return "Reddit page updated!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port, debug=True)
