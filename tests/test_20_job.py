from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository
from lib.scenario import Scenario
from lib.job import Job


REPO = Repository(DB)
REPO.name = 'another_random_repo_name'
REPO.save()

SCENARIO = Scenario(DB)
SCENARIO.name = 'random_scenario'
SCENARIO.repo = REPO.name
SCENARIO.data = '#!/bin/bash\nsleep 1\necho done'
SCENARIO.save()

JOB = Job(DB)
JOB.repo = REPO.name
JOB.scenario = SCENARIO.name


def test_load_absent():
    job = Job(DB, name='missing_name', repo_name=REPO.name, scenario_name=SCENARIO.name)
    assert_equals(job.exists, False)

def test_save():
    job = Job(DB, repo_name=REPO.name, scenario_name=SCENARIO.name)
    result = job.save()
    assert_equals(type(result), dict)

def test_load_present():
    job = Job(DB, repo_name=REPO.name, scenario_name=SCENARIO.name)
    job.save()
    name = job.name
    job = Job(DB, name=name, repo_name=REPO.name, scenario_name=SCENARIO.name)
    assert_equals(job.exists, True)

def test_dump():
    job = Job(DB, repo_name=REPO.name, scenario_name=SCENARIO.name)
    result = job.dump()
    assert_equals(type(result), dict)

# TODO test execution

def test_delete():
    job = Job(DB, repo_name=REPO.name, scenario_name=SCENARIO.name)
    job.save()
    result = job.delete()
    assert_equals(result, True)

def test_cleanup():
    result = []
    result.append(SCENARIO.delete())
    result.append(REPO.delete())
    assert_equals(result, [True, True])
