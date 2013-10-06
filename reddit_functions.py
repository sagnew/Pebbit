import requests
import praw

r = praw.Reddit('Testing')

submission_dict = {}
comment_dict = {}
initial_data = {}
count_dict = {}

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
    if pebble not in count_dict.keys():
        count_dict[pebble] = {}
        count_dict[pebble]['submissions'] = 0
        count_dict[pebble]['comments'] = {}
    if pebble not in submission_dict.keys():
        submission_dict[pebble] = {}
        build_dictionaries(pebble)
    submission_count = count_dict[pebble]['submissions']
    count_dict[pebble]['submissions'] += 1
    return {0: submission_dict[pebble][submission_count]}

def get_comments_by_submission_id(pebble, id):
    if pebble not in count_dict.keys():
        count_dict[pebble] = {}
        count_dict[pebble]['submissions'] = 0
        count_dict[pebble]['comments'] = {}
    if pebble not in comment_dict.keys():
        comment_dict[pebble] = {}
        build_dictionaries(pebble)
    if id not in count_dict[pebble]['comments'].keys():
        count_dict[pebble]['comments'][id] = 0
    comment_count = count_dict[pebble]['comments'][id]
    count_dict[pebble]['comments'][id] += 1
    return {0: comment_dict[pebble][id][1][comment_count]}

cache_initial_data()
