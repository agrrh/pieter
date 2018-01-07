import uuid
import asyncio
import subprocess
import time
import os


class Job(object):
    def __init__(self, db, name=None):
        self.db = db

        # Event loop
        self.loop = None

        self.__build()
        self.name = str(uuid.uuid4())

    def __build(self):
        """Initialize properties."""
        self.name = None
        self.state = None
        self.repo = None
        self.scenario = None
        self.time_start = None
        self.time_done = None
        self.stdout = None
        self.stderr = None
        self.rc = None

    async def background(self, script_path):
        """Run process in background."""
        process = await asyncio.create_subprocess_exec(script_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        self.time_done = int(time.time())
        self.stdout = stdout.decode()
        self.stderr = stderr.decode()
        self.rc = process.returncode

    async def execute(self, scenario_data):
        """Prepare and fire off a job."""
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
        task = loop.create_task(self.background(job_script_path))
        task.add_done_callback(self.save)

    def load(self, name=None):
        """Populate properties with values from DB."""
        if name and not self.db.exists('job', name or self.name):
            return False

        data = self.db.read('job', name or self.name)

        if data:
            self.name = name or self.name
            self.state = data['state']
            self.repo = data['repo'] or self.repo
            self.scenario = data['scenario'] or self.scenario
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

    def save(self, *args):
        """Write object to database."""
        return self.db.update('job', self.name, self.dump(), ttl=3600)

    def dump(self):
        """Provide object as dict."""
        return {
            'name': self.name,
            'state': self.state,
            'repo': self.repo,
            'scenario': self.scenario,
            'time_start': self.time_start,
            'time_done': self.time_done,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'rc': self.rc
        }

    def delete(self):
        """Remove from database and nullify values."""
        name_unique = '/'.join((self.repo, self.scenario, self.name))
        self.db.delete('scenario', name_unique)
        self.__build()
