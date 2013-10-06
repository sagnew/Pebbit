import requests
import praw

r = praw.Reddit('Testing')

submission_dict = {}
comment_dict = {}

def build_dictionaries():
    """
    comment_dict[id][0] = submission title
    comment_dict[id[[1] = array of comments
    """
    submissions = r.get_subreddit('all')

    count = 0
    for submission in submissions.get_top(limit=5):
        submission_dict[count] = submission.title
        comment_dict[count] = {}
        comment_dict[count][0] = submission.title
        comment_dict[count][1] = []
        for comment in submission.comments:
            comment_dict[count]['comments'].append(comment.__str__())
        count += 1

def get_submission_dict():
    return submission_dict

def get_comments_by_submission_id(id):
    return comment_dict[id]

def get_comment_dict():
    return comment_dict

build_dictionaries()
