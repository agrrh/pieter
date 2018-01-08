from nose.tools import assert_equals
import json

from lib.webhook import Webhook


def test_github_payload():
    w = Webhook(json.load(open('tests/static/github_payload.json')))
    assert_equals(w.author, 'baxterthehacker')

def test_gitea_payload():
    w = Webhook(json.load(open('tests/static/gitea_payload.json')))
    assert_equals(w.author, 'Gitea')

def test_gogs_payload():
    w = Webhook(json.load(open('tests/static/gogs_payload.json')))
    assert_equals(w.author, 'Unknwon')

def test_gitlab_payload():
    w = Webhook(json.load(open('tests/static/gitlab_payload.json')))
    assert_equals(w.author, 'GitLab dev user')
