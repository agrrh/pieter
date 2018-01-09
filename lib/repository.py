from lib.baseobject import BaseObject


class Repository(BaseObject):
    def __init__(self, name, data=None, db=None):
        super(Repository, self).__init__('repo', name, db=db)

        self.name_unique = name
        self.build(data)

    def build(self, data=None):
        super(Repository, self).build(data)

        self.scenarios = getattr(self, 'scenarios', [])
        self.latest_job = getattr(self, 'latest_job', None)
