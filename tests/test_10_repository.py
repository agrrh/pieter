from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository


def test_load_absent():
    repo = Repository(DB, 'absent')
    assert_equals(repo.exists, False)

def test_save():
    repo = Repository(DB, 'some_random_name_for_present_repo')
    result = repo.save()
    assert_equals(type(result), dict)

def test_load_present():
    repo = Repository(DB, 'some_random_name_for_present_repo')
    assert_equals(repo.exists, True)

def test_dump():
    repo = Repository(DB, 'some_random_name_for_present_repo')
    result = repo.dump()
    assert_equals(type(result), dict)

def test_delete():
    repo = Repository(DB, 'some_random_name_for_present_repo')
    result = repo.delete()
    assert_equals(result, True)
