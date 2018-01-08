import json


class Webhook(object):
    def __init__(self, data):
        if not data:
            return None

        self.ref = data['ref']
        self.branch = self.ref.split('/')[-1] if '/' in self.ref else None
        self.commit = data['commits'][-1]['id']
        self.commit_url = data['commits'][-1]['url']
        self.message = data['commits'][-1]['message']
        self.author = data['commits'][-1]['author']['name']

    def dump(self):
        data = {
            'ref': self.ref,
            'branch': self.branch,
            'commit': self.commit,
            'commit_url': self.commit_url,
            'message': self.message,
            'author': self.author
        }
        return json.dumps(data)
