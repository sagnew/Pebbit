import requests
import praw

r = praw.Reddit('Testing')

def get_submission_dict():
    submissions = r.get_subreddit('all')

    reddit_dict = {}
    for submission in submissions.get_top(limit=10):
        reddit_dict[submission.title] = []
        for comment in submission.comments:
            reddit_dict[submission.title].append(comment.__str__())

    return reddit_dict
