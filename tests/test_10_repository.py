from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository


def test_load_absent():
    repo = Repository('absent', db=DB)
    repo.load()
    assert_equals(repo.exists, False)

def test_save():
    repo = Repository('some_random_name_for_present', db=DB)
    repo.property = 'test_value'
    result = repo.save()
    assert_equals(type(result), dict)

def test_load_present():
    repo = Repository('some_random_name_for_present', db=DB)
    repo.load()
    print(repo.dump())
    assert_equals([repo.exists, repo.property], [True, 'test_value'])

def test_dump():
    repo = Repository('some_random_name_for_present')
    assert_equals(type(repo.dump()), dict)

def test_delete():
    repo = Repository('some_random_name_for_present', db=DB)
    result = repo.delete()
    assert_equals(result, True)
