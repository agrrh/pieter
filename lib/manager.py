from lib.repository import Repository
from lib.scenario import Scenario
from lib.job import Job


class Manager(object):
    """Provide interaction between BaseObjects: repos, scenarios, etc."""
    def __init__(self, db):
        self.db = db

    def repos_list(self):
        # Cut off "repo_" from repos unique names
        return [repo_name[5:] for repo_name in self.db.list('repo_*')]

    def repo_load(self, repo_name):
        repo = Repository(repo_name, db=self.db)
        repo.load()
        return repo

    def repo_update(self, repo_name, data):
        repo = Repository(repo_name, data=data, db=self.db)
        repo.save()
        return repo

    def repo_delete(self, repo_name):
        repo = Repository(repo_name, db=self.db)
        repo.delete()
        return repo

    def scenario_load(self, scenario_name, repo):
        scenario = Scenario(scenario_name, repo=repo, db=self.db)
        scenario.load()
        return scenario

    def scenario_update(self, scenario_name, repo, data):
        scenario = Scenario(scenario_name, repo, data=data, db=self.db)
        scenario.save()
        if scenario.name not in repo.scenarios:
            repo.scenarios.append(scenario.name)
            repo.save()
        return scenario

    def scenario_delete(self, scenario_name, repo):
        scenario = Scenario(scenario_name, repo=repo, db=self.db)
        scenario.delete()
        if scenario.name in repo.scenarios:
            repo.scenarios.remove(scenario.name)
            repo.save()
        return scenario

    async def job_run(self, repo, scenario, hook_data=None):
        job = Job(None, repo, scenario, db=self.db)
        await job.execute(scenario.data, hook_data=hook_data)
        repo.latest_job = job.name
        repo.save()
        scenario.latest_job = job.name
        scenario.save()
        return job

    def job_load(self, job_name):
        job_data = self.db.read('job', job_name)
        if not job_data:
            return False
        repo = Repository(job_data['repo'], db=self.db)
        scenario = Scenario(job_data['scenario'], repo=repo, db=self.db)
        job = Job(job_name, repo, scenario, db=self.db)
        job.load()
        return job

    def job_delete(self, job_name):
        job_data = self.db.read('job', job_name)
        if not job_data:
            return False
        repo = Repository(job_data['repo'], db=self.db)
        scenario = Scenario(job_data['scenario'], repo=repo, db=self.db)
        job = Job(job_name, repo, scenario, db=self.db)
        job.delete()
        return job
