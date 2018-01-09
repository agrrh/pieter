from nose.tools import assert_equals
from tests.common import API_URL

import time
import requests


def __time():
    return str(int(time.time()))

REPO_NAME = 'automated_tests' + __time()

def test_repos_list():
    result = requests.get(API_URL + 'repos')
    assert_equals(type(result.json()), list)

def test_repos_get_absent():
    result = requests.get(API_URL + 'repos/' + REPO_NAME)
    assert_equals(result.status_code, 404)

def test_repos_write():
    result = requests.put(API_URL + 'repos/' + REPO_NAME, json={'source': 'git@github.com:agrrh/pieter-ci.git'})
    assert_equals(result.status_code, 201)

def test_repos_get_present():
    result = requests.get(API_URL + 'repos/' + REPO_NAME)
    assert_equals(type(result.json()), dict)

def test_repos_delete():
    result = []
    result.append(requests.put(
        API_URL + 'repos/automated_tests_todelete',
        json={'source': 'git@github.com:agrrh/pieter-ci.git'}
    ))
    result.append(requests.delete(API_URL + 'repos/automated_tests_todelete'))
    result.append(requests.get(API_URL + 'repos/automated_tests_todelete'))

    assert_equals([r.status_code for r in result], [201, 200, 404])

def test_scenario_get_absent():
    result = requests.get(API_URL + 'repos/' + REPO_NAME + '/scenario_absent')
    assert_equals(result.status_code, 404)

def test_scenario_write():
    data = open('misc/test_script.sh', 'rb').read()
    result = requests.put(API_URL + 'repos/' + REPO_NAME + '/scenario1', data=data)
    assert_equals(result.status_code, 201)

def test_scenario_update():
    data = open('misc/test_script.sh', 'rb').read()
    result = requests.put(API_URL + 'repos/' + REPO_NAME + '/scenario1', data=data)
    assert_equals(result.status_code, 200)

def test_scenario_get_present():
    result = requests.get(API_URL + 'repos/' + REPO_NAME + '/scenario1')
    assert_equals(type(result.json()), dict)

def test_job_start_manual():
    result = requests.patch(API_URL + 'repos/' + REPO_NAME + '/scenario1')
    assert_equals(result.status_code, 201)

def test_job_latest_name():
    result = requests.patch(API_URL + 'repos/' + REPO_NAME + '/scenario1')
    latest_job_name = result.json()['name']
    result = requests.get(API_URL + 'repos/' + REPO_NAME + '/scenario1')
    assert_equals(result.json()['latest_job'], latest_job_name)

def test_job_delete():
    result = requests.get(API_URL + 'repos/' + REPO_NAME + '/scenario1')
    latest_job_name = result.json()['latest_job']
    result = requests.delete(API_URL + 'jobs/' + latest_job_name)
    assert_equals(result.status_code, 200)

def test_scenario_mentioned_in_repo():
    repo = requests.get(API_URL + 'repos/' + REPO_NAME)
    result = 'scenario1' in repo.json()['scenarios']
    assert_equals(result, True)

"""
def test_scenario_delete():
    result = requests.delete(API_URL + 'repos/' + REPO_NAME + '/scenario1')
    assert_equals(result.status_code, 200)

def test_scenario_missing_in_repo():
    repo = requests.get(API_URL + 'repos/' + REPO_NAME)
    result = 'scenario1' in repo.json()['scenarios']
    assert_equals(result, False)

def test_cleanup():
    result = requests.delete(API_URL + 'repos/' + REPO_NAME)
    assert_equals(result.status_code, 200)
"""
