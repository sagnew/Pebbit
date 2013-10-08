import requests
import praw

class RedditRetriever():


    def __init__(self):
        self.submission_dict = {}
        self.comment_dict = {}
        self.initial_data = {}
        self.count_dict = {}

    def cache_initial_data(self):
        r = praw.Reddit('Testing')
        submissions = r.get_subreddit('all')
        self.initial_data['submissions'] = {}
        self.initial_data['comments'] = {}

        count = 0
        for submission in submissions.get_top(limit=25):
            self.initial_data['submissions'][count] = submission.title
            self.initial_data['comments'][count] = {}
            self.initial_data['comments'][count][0] = submission.title
            self.initial_data['comments'][count][1] = []
            comment_count = 0
            for comment in submission.comments:
                if comment_count > 10:
                    break
                self.initial_data['comments'][count][1].append(comment.__str__())
                comment_count += 1
            count += 1


    def build_dictionaries(self, pebble):
        """
        comment_dict[id][0] = submission title
        comment_dict[id[[1] = array of comments
        """

        if pebble not in self.comment_dict.keys():
            self.comment_dict[pebble] = {}
        self.comment_dict[pebble] = self.initial_data['comments']
        if pebble not in self.submission_dict.keys():
            self.submission_dict[pebble] = {}
        self.submission_dict[pebble] = self.initial_data['submissions']

    def get_submission_dict(self, pebble):
        if pebble not in self.count_dict.keys():
            self.count_dict[pebble] = {}
            self.count_dict[pebble]['submissions'] = 0
            self.count_dict[pebble]['comments'] = {}
        if pebble not in self.submission_dict.keys():
            self.submission_dict[pebble] = {}
            self.build_dictionaries(pebble)
        submission_count = self.count_dict[pebble]['submissions']
        self.count_dict[pebble]['submissions'] += 1
        return {0: self.submission_dict[pebble][submission_count]}

    def get_comments_by_submission_id(self, pebble, id):
        if pebble not in self.count_dict.keys():
            self.count_dict[pebble] = {}
            self.count_dict[pebble]['submissions'] = 0
            self.count_dict[pebble]['comments'] = {}
        if pebble not in self.comment_dict.keys():
            self.comment_dict[pebble] = {}
            self.build_dictionaries(pebble)
        if id not in self.count_dict[pebble]['comments'].keys():
            self.count_dict[pebble]['comments'][id] = 0
        comment_count = self.count_dict[pebble]['comments'][id]
        self.count_dict[pebble]['comments'][id] += 1
        return {0: self.comment_dict[pebble][id][1][comment_count]}
