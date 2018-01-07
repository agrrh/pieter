import os


class Scenario(object):
    def __init__(self, repo, name):
        self.repo = repo

        self.name = name

        self.path = '/'.join(('scenario', self.repo.name, self.name))
        self.exists = os.path.isfile(self.path)
        self.data = open(self.path, 'r').read() if self.exists else None

    def create(self, data):
        dir_path = os.path.dirname(self.path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, mode=0o750)
        with open(self.path, 'wb') as fp:
            fp.write(data)
        os.chmod(self.path, 0o775)
        self.data = data
        self.exists = True

    def read(self):
        return {
            'name': self.name,
            'repo': self.repo.name,
            'path': self.path,
            'exists': self.exists,
            'data': self.data
        }

    update = create

    def delete(self):
        os.remove(self.path)
        self.data = None
        self.exists = False
