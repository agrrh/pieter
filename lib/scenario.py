import os


class Scenario(object):
    def __init__(self, db, name=None, repo_name=None):
        self.db = db

        self.__build()

        if name and repo_name:
            self.exists = self.load(name=name, repo_name=repo_name)

    def __build(self):
        """Initialize properties."""
        self.exists = False
        self.name = None
        self.repo = None
        self.data = None
        self.latest_job = None

    def load(self, name=None, repo_name=None):
        """Populate properties with values from DB."""
        self.name = name or self.name
        self.repo = repo_name or self.repo

        name_unique = '{}/{}'.format(repo_name, name or self.name)
        if name and not self.db.exists('scenario', name_unique):
            return False

        data = self.db.read('scenario', name_unique)

        self.repo = data['repo']
        self.data = data['data']
        self.latest_job = data['latest_job'] if 'latest_job' in data else None

        return True

    def save(self):
        """Write object to database."""
        self.exists = True
        name_unique = '{}/{}'.format(self.repo, self.name)
        return self.db.update('scenario', name_unique, self.dump())

    def dump(self):
        """Provide object as dict."""
        return {
            'exists': self.exists,
            'name': self.name,
            'repo': self.repo,
            'data': self.data,
            'latest_job': self.latest_job
        }

    def delete(self):
        """Remove from database and nullify values."""
        name_unique = '{}/{}'.format(self.repo, self.name)
        result = self.db.delete('scenario', name_unique)
        self.__build()
        return bool(result)
