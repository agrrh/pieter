import os

from sanic import Sanic
from sanic import response

from lib.db_redis import Database
from lib.manager import Manager


class API(object):
    def __init__(self):
        self.app = Sanic('pieter', load_env='PIETER_')

        self.db = Database(
            host=self.app.config.DB_HOST,
            port=self.app.config.DB_PORT
        )
        self.manager = Manager(self.db)

        self.routes_define()

    def routes_define(self):
        @self.app.route("/")
        async def index(request):
            # TODO automate it
            result = response.json((
                'GET /repos',
                'GET /repos/<repo_name>',
                'PUT /repos/<repo_name>',
                'DELETE /repos/<repo_name>',
                'PUT /repos/<repo_name>/<scenario_name>',
                'GET /repos/<repo_name>/<scenario_name>',
                'DELETE /repos/<repo_name>/<scenario_name>',
                'PATCH /repos/<repo_name>/<scenario_name>',
                'GET /jobs/<uuid>',
                'POST /webhooks/<repo_name>/<scenario_name>'
            ))

            return result

        @self.app.route("/repos", methods=['GET'])
        async def repos_index(request):
            return response.json(self.manager.repos_list())

        @self.app.route("/repos/<repo_name>", methods=['GET', 'PUT', 'DELETE'])
        async def repo_actions(request, repo_name):
            if request.method == 'GET':
                repo = self.manager.repo_load(repo_name)
                result = response.json(repo.dump(), status=200) \
                    if repo.exists \
                    else response.json('Repo not found', status=404)

            elif request.method == 'PUT':
                repo = self.manager.repo_load(repo_name)
                result = response.json(repo.dump(), status=201) \
                    if self.manager.repo_update(repo_name, request.json) \
                    else response.json('Failed to update repo', status=500)

            elif request.method == 'DELETE':
                repo = self.manager.repo_load(repo_name)
                if repo.exists:
                    if self.manager.repo_delete(repo_name):
                        result = response.json(repo.dump(), status=200)
                    else:
                        result = response.json('Failed to delet repo', status=500)
                else:
                    response.json('Repo not found', status=404)

            return result

        @self.app.route("/repos/<repo_name>/<scenario_name>", methods=['PUT', 'GET', 'DELETE', 'PATCH'])
        async def scenario_actions(request, repo_name, scenario_name):
            repo = self.manager.repo_load(repo_name)
            scenario = self.manager.scenario_load(scenario_name, repo=repo)

            if request.method == 'PUT':
                if len(request.body) < 4 or len(request.body) > 10240:
                    result = response.json('File size does not match sane limits', status=400)
                else:
                    code = 200 if scenario.exists else 201
                    scenario = self.manager.scenario_update(
                        scenario_name, repo=repo, data={'data': request.body.decode()}
                    )
                    result = response.json(scenario.dump(), status=code)

            elif request.method == 'GET':
                if scenario.exists:
                    result = response.json(scenario.dump())
                else:
                    result = response.json('Scenario not found', status=404)

            elif request.method == 'DELETE':
                if scenario.exists:
                    scenario = self.manager.scenario_delete(scenario_name, repo=repo)
                    result = response.json(scenario.dump())
                else:
                    result = response.json('Scenario not found', status=404)

            elif request.method == 'PATCH':
                if scenario.exists:
                    job = await self.manager.job_run(repo, scenario)
                    result = response.json(job.dump(), status=201)
                else:
                    result = response.json('Scenario not found', status=404)

            return result

        @self.app.route("/jobs/<job_name>", methods=['GET', 'DELETE'])
        async def job_actions(request, job_name):
            job = self.manager.job_load(job_name)

            if request.method == 'GET':
                if job and job.exists:
                    result = response.json(job.dump())
                else:
                    result = response.json('Job not found', status=404)
            elif request.method == 'DELETE':
                if job and job.exists:
                    job = self.manager.job_delete(job_name)
                    result = response.json(job.dump())
                else:
                    result = response.json('Job not found', status=404)

            return result

        @self.app.route("/webhooks/<repo_name>/<scenario_name>", methods=['POST'])
        async def webhooks(request, repo_name, scenario_name):
            is_github = 'X-GitHub-Event' in request.headers
            is_gitlab = 'X-Gitlab-Event' in request.headers
            event_type = request.headers['X-GitHub-Event'] or request.headers['X-Gitlab-Event']
            pusher_recieved = request.json.get('pusher')

            headers_ok = is_github or is_gitlab
            pusher_ok = pusher_recieved and 'push' in event_type.lower()
            ping_ok = 'ping' in event_type.lower()

            if ping_ok:
                result = response.json('Pong', 200)
            elif not headers_ok or not pusher_ok:
                result = response.json('Malformed request, check "pusher" data and headers', 400)
            else:
                repo = self.manager.repo_load(repo_name)
                scenario = self.manager.scenario_load(scenario_name, repo=repo)

                if not repo.exists:
                    result = response.json('Repo not found', 404)
                elif not scenario.exists:
                    result = response.json('Scenario not found', 404)
                else:
                    job = await self.manager.job_run(repo, scenario)
                    result = response.json(job.dump(), status=201)

            return result

    def run(self):
        self.app.run(
            host=self.app.config.API_HOST,
            port=self.app.config.API_PORT
        )
