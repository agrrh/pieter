import uuid
import asyncio
import time
import os

from lib.webhook import Webhook
from lib.baseobject import BaseObject


class Job(BaseObject):
    def __init__(self, name, repo, scenario, data=None, db=None):
        if name is None:
            name = str(uuid.uuid4())

        super(Job, self).__init__('job', name, db=db)

        self.repo = repo.name
        self.scenario = scenario.name

        self.name_unique = name
        self.build(data)

    def build(self, data=None):
        super(Job, self).build(data)

        self.state = getattr(self, 'state', 'created')
        self.timestamp = getattr(self, 'timestamp', None)
        self.stdout = getattr(self, 'stdout', None)
        self.stderr = getattr(self, 'stderr', None)
        self.rc = getattr(self, 'rc', None)

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

        self.duration = time.time() - self.timestamp
        self.stdout = stdout.decode()
        self.stderr = stderr.decode()
        self.rc = process.returncode

    async def execute(self, scenario_data, hook_data=None):
        """Prepare and fire off a job."""
        self.state = 'running'
        self.timestamp = time.time()

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
