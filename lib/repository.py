import os

from lib.scenario import Scenario


class Repository(object):
    def __init__(self, db):
        self.db = db

        self.__build()

    def __build(self):
        """Initialize properties."""
        self.name = None
        self.source = None
        self.scenarios = None

    def load(self, name=None):
        """Populate properties with values from DB."""
        if name and not self.db.exists('repo', name):
            return False

        data = self.db.read('repo', name or self.name)

        self.name = name or self.name
        self.source = data['source']
        self.scenarios = data['scenarios']  # TODO use redis lists?

        return True

    def save(self):
        """Write object to database."""
        return self.db.update('repo', self.name, self.dump())

    def dump(self):
        """Provide object as dict."""
        return {
            'name': self.name,
            'source': self.source,
            'scenarios': self.scenarios
        }

    def delete(self):
        """Remove from database and nullify values."""
        self.db.delete('repo', self.name)
        self.__build()
