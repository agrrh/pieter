import os

from lib.scenario import Scenario


class Repository(object):
    def __init__(self, db, name=None):
        self.db = db

        self.__build()

        if name:
            self.exists = self.load(name)

    def __build(self):
        """Initialize properties."""
        self.exists = False
        self.name = None
        self.source = None
        self.scenarios = None

    def load(self, name=None):
        """Populate properties with values from DB."""
        self.name = name or self.name
        
        if name and not self.db.exists('repo', name):
            return False

        data = self.db.read('repo', name or self.name)

        self.source = data['source']
        self.scenarios = data['scenarios']  # TODO use redis lists?

        return True

    def save(self):
        """Write object to database."""
        self.exists = True
        return self.db.update('repo', self.name, self.dump())

    def dump(self):
        """Provide object as dict."""
        return {
            'exists': self.exists,
            'name': self.name,
            'source': self.source,
            'scenarios': self.scenarios
        }

    def delete(self):
        """Remove from database and nullify values."""
        result = self.db.delete('repo', self.name)
        self.__build()
        return bool(result)
