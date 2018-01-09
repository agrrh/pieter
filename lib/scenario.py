from lib.baseobject import BaseObject


class Scenario(BaseObject):
    def __init__(self, name, repo, data=None, db=None):
        super(Scenario, self).__init__('scenario', name, db=db)

        self.repo = repo.name

        self.name_unique = '/'.join((repo.name, name))
        self.build(data)

    def build(self, data=None):
        super(Scenario, self).build(data)

        self.data = getattr(self, 'data', None)
        self.latest_job = getattr(self, 'latest_job', None)
