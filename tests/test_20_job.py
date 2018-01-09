from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository
from lib.scenario import Scenario
from lib.job import Job


REPO = Repository('another_random_repo_name', db=DB)
REPO.save()

SCENARIO = Scenario('random_scenario', REPO, db=DB)
SCENARIO.data = '#!/bin/bash\nsleep 1\necho done'
SCENARIO.save()


def test_load_absent():
    job = Job('missing_name', REPO, SCENARIO, db=DB)
    job.load()
    assert_equals(job.exists, False)

def test_save():
    job = Job('present_name', REPO, SCENARIO, db=DB)
    job.attribute = 51
    result = job.save()
    assert_equals(type(result), dict)

def test_load_present():
    job = Job('present_name', REPO, SCENARIO, db=DB)
    job.load()
    assert_equals(job.attribute, 51)

def test_dump():
    job = Job('present_name', REPO, SCENARIO, db=DB)
    result = job.dump()
    assert_equals(type(result), dict)

# TODO test execution

def test_delete():
    job = Job('present_name', REPO, SCENARIO, db=DB)
    result = job.delete()
    assert_equals(result, True)

def test_cleanup():
    result = []
    result.append(SCENARIO.delete())
    result.append(REPO.delete())
    assert_equals(result, [True, True])
