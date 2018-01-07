import os


class Scenario(object):
    def __init__(self, db):
        self.db = db

        self.__build()

    def __build(self):
        """Initialize properties."""
        self.name = None
        self.repo = None
        self.data = None

    def load(self, name=None, repo_name=None):
        """Populate properties with values from DB."""
        name_unique = '{}/{}'.format(repo_name, name or self.name)

        if name and not self.db.exists('scenario', name_unique):
            return False

        data = self.db.read('scenario', name_unique)

        self.name = name
        self.repo = data['repo']
        self.data = data['data']

        return True

    def save(self):
        """Write object to database."""
        name_unique = '{}/{}'.format(self.repo, self.name)
        return self.db.update('scenario', name_unique, self.dump())

    def dump(self):
        """Provide object as dict."""
        return {
            'name': self.name,
            'repo': self.repo,
            'data': self.data
        }

    def delete(self):
        """Remove from database and nullify values."""
        name_unique = '{}/{}'.format(self.repo, self.name)
        result = self.db.delete('scenario', name_unique)
        self.__build()
        return bool(result)
