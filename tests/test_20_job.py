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
SCENARIO.data = '#!/bin/bash\nsleep 2\necho done'
SCENARIO.save()

JOB = Job(DB)
JOB.repo = REPO.name
JOB.scenario = SCENARIO.name


def test_load_absent():
    result = JOB.load('random_missing_name')
    assert_equals(result, False)

def test_save():
    result = JOB.save()
    assert_equals(type(result), dict)

def test_load_present():
    result = JOB.load()
    assert_equals(result, True)

def test_dump():
    result = JOB.dump()
    assert_equals(type(result), dict)

def test_delete():
    JOB.save()
    result = JOB.delete()
    assert_equals(result, True)
