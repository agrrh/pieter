import uuid
import asyncio
import subprocess
import time
import os

from lib.webhook import Webhook


class Job(object):
    def __init__(self, db, name=None, repo_name=None, scenario_name=None):
        self.db = db

        self.__build()

        self.repo = repo_name or self.repo
        self.scenario = scenario_name or self.scenario

        if not name:
            self.name = str(uuid.uuid4())
        elif repo_name and scenario_name:
            self.exists = self.load(name=name, repo_name=repo_name, scenario_name=scenario_name)

    def __build(self):
        """Initialize properties."""
        self.exists = False
        self.name = None
        self.state = 'created'
        self.repo = None
        self.scenario = None
        self.time_start = None
        self.time_done = None
        self.stdout = None
        self.stderr = None
        self.rc = None

    def load(self, name=None, repo_name=None, scenario_name=None):
        """Populate properties with values from DB."""
        self.repo = repo_name or self.repo
        self.scenario = scenario_name or self.scenario

        if name and not self.db.exists('job', name or self.name):
            return False

        data = self.db.read('job', name or self.name)

        if data:
            self.name = name
            self.state = data['state']
            self.repo = data['repo'] or repo_name
            self.scenario = data['scenario'] or scenario_name
            self.time_start = data['time_start']
            self.time_done = data['time_done']
            self.stdout = data['stdout']
            self.stderr = data['stderr']
            self.rc = data['rc']

        if self.rc is not None:
            if self.rc == 0:
                self.state = 'success'
            else:
                self.state = 'fail'

        return True

    def dump(self):
        """Provide object as dict."""
        return {
            'name': self.name,
            'exists': self.exists,
            'state': self.state,
            'repo': self.repo,
            'scenario': self.scenario,
            'time_start': self.time_start,
            'time_done': self.time_done,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'rc': self.rc
        }

    def save(self, *args):
        """Write object to database."""
        self.exists = True
        return self.db.update('job', self.name, self.dump(), ttl=3600)

    def delete(self):
        """Remove from database and nullify values."""
        result = self.db.delete('job', self.name)
        self.__build()
        return bool(result)

    async def background(self, script_path, hook_data=None):
        """Run process in background."""
        if hook_data:
            hook_event = Webhook(hook_data)

        process = await asyncio.create_subprocess_exec(script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        if hook_data:
            await process.communicate(input=hook_event.dump().encode())
        stdout, stderr = await process.communicate()

        self.time_done = int(time.time())
        self.stdout = stdout.decode()
        self.stderr = stderr.decode()
        self.rc = process.returncode

    async def execute(self, scenario_data, hook_data=None):
        """Prepare and fire off a job."""
        self.name = str(uuid.uuid4())
        self.state = 'running'
        self.time_start = int(time.time())

        self.save()

        job_home_path = '/'.join(('jobs', self.name))
        job_script_path = '/'.join((job_home_path, self.scenario))

        os.mkdir(job_home_path, 0o755)
        with open(job_script_path, 'w') as fp:
            fp.write(scenario_data)
        os.chmod(job_script_path, 0o755)

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.background(job_script_path, hook_data=hook_data))
        task.add_done_callback(self.save)
