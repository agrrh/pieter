from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository
from lib.scenario import Scenario


REPO = Repository(DB)
REPO.name = 'random_repo_name'


def test_load_absent():
    scenario = Scenario(DB, 'absent', repo_name=REPO.name)
    assert_equals(scenario.exists, False)

def test_save():
    scenario = Scenario(DB, 'another_random_name_for_present_scenario', repo_name=REPO.name)
    result = scenario.save()
    assert_equals(type(result), dict)

def test_load_present():
    scenario = Scenario(DB, 'another_random_name_for_present_scenario', repo_name=REPO.name)
    assert_equals(scenario.exists, True)

def test_dump():
    scenario = Scenario(DB, 'another_random_name_for_present_scenario', repo_name=REPO.name)
    result = scenario.dump()
    assert_equals(type(result), dict)

def test_delete():
    scenario = Scenario(DB, 'another_random_name_for_present_scenario', repo_name=REPO.name)
    result = scenario.delete()
    assert_equals(result, True)
