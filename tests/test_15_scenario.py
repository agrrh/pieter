from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository
from lib.scenario import Scenario


REPO = Repository('random_repo_name', db=DB)

def test_load_absent():
    scenario = Scenario('absent', REPO, db=DB)
    scenario.load()
    assert_equals(scenario.exists, False)

def test_save():
    scenario = Scenario('some_random_name_for_present', REPO, db=DB)
    scenario.load()
    scenario.data = 42
    result = scenario.save()
    assert_equals(type(result), dict)

def test_load_present():
    scenario = Scenario('some_random_name_for_present', REPO, db=DB)
    scenario.load()
    assert_equals(scenario.data, 42)

def test_dump():
    scenario = Scenario('another_random_name_for_present', REPO)
    result = scenario.dump()
    assert_equals(type(result), dict)

def test_delete():
    scenario = Scenario('some_random_name_for_present', REPO, db=DB)
    result = scenario.delete()
    assert_equals(result, True)
