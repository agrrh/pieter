from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository
from lib.scenario import Scenario


REPO = Repository(DB)
REPO.name = 'random_repo_name'
SCENARIO = Scenario(DB)


def test_load_absent():
    result = SCENARIO.load('absent', repo_name=REPO.name)
    assert_equals(result, False)

def test_save():
    name = 'another_random_name_for_present_scenario'
    SCENARIO.name = name
    result = SCENARIO.save()
    assert_equals(type(result), dict)

def test_load_present():
    name = 'another_random_name_for_present_scenario'
    result = SCENARIO.load(name)
    assert_equals(result, True)

def test_dump():
    result = SCENARIO.dump()
    assert_equals(type(result), dict)

def test_delete():
    result = SCENARIO.delete()
    assert_equals(result, True)
