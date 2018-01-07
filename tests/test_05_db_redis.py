import time

from nose.tools import assert_equals
from tests.common import DB, PREFIX

def __time():
    return str(int(time.time()))

def test_exists_absent():
    result = DB.exists(PREFIX, __time())
    return assert_equals(result, False)

def test_exists_present():
    DB.create(PREFIX, 'present', 'ok')
    result = DB.exists(PREFIX, 'present')
    return assert_equals(result, True)

def test_read():
    result = DB.read(PREFIX, 'present')
    return assert_equals(result, 'ok')

def test_create():
    val = '1st string to write.'
    result = DB.create(PREFIX, 'create', val)
    return assert_equals(result, val)

def test_create_ttl():
    val = '2nd string to write.'
    result = DB.create(PREFIX, 'ttl', val, 1)
    return assert_equals(result, val)

def test_read_ttl():
    time.sleep(2)
    result = DB.read(PREFIX, 'ttl')
    return assert_equals(result, None)

def test_delete():
    result = DB.delete(PREFIX, 'create')
    return assert_equals(result, True)

def test_list():
    result = DB.list(PREFIX + '_*')
    return assert_equals(result, [PREFIX + '_present'])
