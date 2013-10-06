import requests
import praw

r = praw.Reddit('Testing')

submission_dict = {}
comment_dict = {}

initial_data = {}

def cache_initial_data():
    submissions = r.get_subreddit('all')
    initial_data['submissions'] = {}
    initial_data['comments'] = {}

    count = 0
    for submission in submissions.get_top(limit=5):
        initial_data['submissions'][count] = submission.title
        initial_data['comments'][count] = {}
        initial_data['comments'][count][0] = submission.title
        initial_data['comments'][count][1] = []
        comment_count = 0
        for comment in submission.comments:
            if comment_count > 10:
                break
            initial_data['comments'][count][1].append(comment.__str__())
            comment_count += 1
        count += 1


def build_dictionaries(pebble):
    """
    comment_dict[id][0] = submission title
    comment_dict[id[[1] = array of comments
    """

    if pebble not in comment_dict.keys():
        comment_dict[pebble] = {}
    comment_dict[pebble] = initial_data['comments']
    if pebble not in submission_dict.keys():
        submission_dict[pebble] = {}
    submission_dict[pebble] = initial_data['submissions']

def get_submission_dict(pebble):
    if pebble not in submission_dict.keys():
        submission_dict[pebble] = {}
        build_dictionaries(pebble)
    return submission_dict[pebble]

def get_comments_by_submission_id(pebble, id):
    if pebble not in comment_dict.keys():
        comment_dict[pebble] = {}
        build_dictionaries(pebble)
    return comment_dict[pebble][id]

def get_comment_dict():
    return comment_dict

cache_initial_data()
