class BaseObject(object):
    """Base object class."""
    def __init__(self, type_, name, db=None):
        self.type = type_
        self.name = name
        self.name_unique = None

        if db is not None:
            self.db = db

        self.build()

    def build(self, data=None):
        if data is None:
            self.exists = False

        elif type(data) is dict:
            self.exists = True
            [setattr(self, k, data[k]) for k in data]

    def dump(self):
        data = dict(self.__dict__)

        data.pop('type', None)
        data.pop('exists', None)
        data.pop('name_unique', None)
        data.pop('db', None)

        return data

    def load(self):
        data = self.db.read(self.type, self.name_unique)
        self.build(data)
        return data

    def save(self, data=None):
        if data is None:
            data = self.dump()
        return self.db.update(self.type, self.name_unique, data)

    def delete(self):
        self.build(None)
        return self.db.delete(self.type, self.name_unique)
