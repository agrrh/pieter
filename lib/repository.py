import os
import yaml

from lib.scenario import Scenario


class Repository(object):
    def __init__(self, name):
        self.name = name

        self.path = '/'.join(('scenario', self.name))

        data_file = './data.yml'
        data_file_exists = os.path.exists(data_file)
        data = yaml.load(open(data_file))
        repo_is_in_data_file = 'repos' in data and self.name in data['repos']

        self.exists = True if (
            data_file_exists and repo_is_in_data_file
        ) else False

        # TODO add source property here

        self.source = None

        self.scenarios = list(os.walk(self.path))[0][1] \
            if os.path.isdir(self.path) \
            else []

    def create(self, source):
        self.source = source

        data_file = './data.yml'
        data = yaml.load(open(data_file))
        data['repos'][self.name] = self.read()
        with open(data_file, 'w') as fp:
            fp.write(yaml.dump(data, default_flow_style=False))
        self.exists = True

    def read(self):
        return {
            'name': self.name,
            'path': self.path,
            'exists': self.exists,
            'scenarios': self.scenarios
        }

    update = create

    def delete(self):
        data_file = './data.yml'
        data = yaml.load(open(data_file))
        data['repos'].pop(self.name, None)
        for s in self.scenarios:
            scenario = Scenario(self, s)
            scenario.delete()
        self.exists = False
        with open(data_file, 'w') as fp:
            fp.write(yaml.dump(data, default_flow_style=False))
