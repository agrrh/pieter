from nose.tools import assert_equals
from tests.common import DB, PREFIX

from lib.repository import Repository


REPO = Repository(DB)


def test_load_absent():
    result = REPO.load('absent')
    assert_equals(result, False)

def test_save():
    name = 'some_random_name_for_present_repo'
    REPO.name = name
    result = REPO.save()
    assert_equals(type(result), dict)

def test_load_present():
    name = 'some_random_name_for_present_repo'
    result = REPO.load(name)
    assert_equals(result, True)

def test_dump():
    result = REPO.dump()
    assert_equals(type(result), dict)

def test_delete():
    result = REPO.delete()
    assert_equals(result, True)
