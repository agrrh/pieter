import uuid
import subprocess
import time
import os


class Job(object):
    def __init__(self, name=None):
        if name is None:
            self.name = str(uuid.uuid4())
        else:
            self.name = name

        self.log_path = 'logs/{}.out.log'.format(self.name)
        self.err_path = 'logs/{}.err.log'.format(self.name)
        self.log_fp = open(self.log_path, 'a')
        self.err_fp = open(self.err_path, 'a')

        self.state_path = 'logs/{}.state'.format(self.name)
        self.state = None if not os.path.exists(self.state_path) else 'running'

        if name is None:
            self.time_start = self._get_job_time_start()
            self.time_done = None
            self.duration = None
            self.rc = None
            self.log = None
            self.err = None
        else:
            self.time_start = self._get_job_time_start(self.state_path)
            self.rc, self.time_done = self._get_job_result()
            self.duration = self.time_done - self.time_start if self.time_done else None
            self.log = self._get_file_contents(self.log_path)
            self.err = self._get_file_contents(self.err_path)

    def _get_job_time_start(self, path=None):
        if path and os.path.isfile(path):
            data = int(os.path.getmtime(path))
        else:
            data = int(time.time())
        return data

    def _get_file_contents(self, path):
        if os.path.isfile(path):
            data = open(path, 'r').read()
        else:
            data = None
        return data

    def _get_job_result(self):
        try:
            data = open(self.state_path, 'r').read().strip()
            rc, time_done = data.split(';')
            rc = int(rc)
            time_done = int(time_done)
            self.state = 'done'
        except:
            rc = None
            time_done = None
        return rc, time_done

    def create(self, scenario_path):
        self.state = 'running'
        subprocess.Popen(
            'bash job.sh {} {} {}'.format(self.name, scenario_path, self.state_path),
            shell=True, stdout=self.log_fp, stderr=self.err_fp
        )

    def read(self):
        self.rc, self.time_done = self._get_job_result()
        self.log = self._get_file_contents(self.log_path)
        self.err = self._get_file_contents(self.err_path)
        return {
            'name': self.name,
            'state': self.state,
            'time_start': self.time_start,
            'time_done': self.time_done,
            'duration': self.duration,
            'log_path': self.log_path,
            'err_path': self.err_path,
            'state_path': self.state_path,
            'log': self.log,
            'err': self.err,
            'rc': self.rc
        }

    def delete(self):
        files = (
            self.log_path,
            self.err_path,
            self.state_path
        )
        for f in files:
            os.remove(f)

        self.time_start = None
        self.time_done = None
        self.duration = None

        self.log = None
        self.err = None

        self.rc = None

        self.state = None
