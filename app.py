from flask import Flask
from flask import request
from flask import redirect
import os
import json

from reddit_functions import get_submission_dict

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main_page():
    return json.dumps(get_submission_dict())

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port, debug=True)
