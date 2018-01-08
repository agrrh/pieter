import os

from sanic import Sanic
from sanic import response

from lib.db_redis import Database

from lib.repository import Repository
from lib.scenario import Scenario
from lib.job import Job


class API(object):
    def __init__(self):
        self.app = Sanic('pieter', load_env='PIETER_')

        self.db = Database(
            host=self.app.config.DB_HOST,
            port=self.app.config.DB_PORT
        )

        self.routes_define()

    def routes_define(self):
        @self.app.route("/")
        async def index(request):
            result = response.json((
                # Get repos list
                'GET /repos',

                # Get repo info
                'GET /repos/<repo_name>',
                # Create/update repo
                'PUT /repos/<repo_name>',
                # Delete particular repo
                'DELETE /repos/<repo_name>',

                # Create/update scenario for repo
                'PUT /repos/<repo_name>/<scenario_name>',
                # Get scenario info
                'GET /repos/<repo_name>/<scenario_name>',
                # Delete scenario
                'DELETE /repos/<repo_name>/<scenario_name>',
                # Execute scenario
                'PATCH /repos/<repo_name>/<scenario_name>',

                # Check job status
                'GET /jobs/<uuid>',
                # Get latest job for repo/scenario
                'GET /repos/<repo_name>/<scenario_name>/jobs/latest',

                # VCS webhooks endpoint
                'POST /webhooks/<repo_name>/<scenario_name>'
            ))

            return result

        @self.app.route("/repos", methods=['GET'])
        async def repos_index(request):
            repos_list = self.db.list('repo_*')
            # Cleaning up "repo_" prefix
            repos_list = [repo_name[5:] for repo_name in repos_list]
            return response.json(repos_list)

        @self.app.route("/repos/<repo_name>", methods=['GET', 'PUT', 'DELETE'])
        async def repo_actions(request, repo_name):
            repo = Repository(self.db, name=repo_name)

            if request.method == 'GET':
                if not repo.exists:
                    result = response.json(None, status=404)
                else:
                    result = response.json(repo.dump())

            elif request.method == 'PUT':
                if not request.json or 'source' not in request.json:
                    result = response.json('Provide "source" with git URL', status=400)
                else:
                    source = request.json['source']

                    repo.name = repo_name
                    repo.scenarios = []

                    repo_old = repo.dump()
                    repo.source = source
                    repo.save()
                    repo_new = repo.dump()

                    code = 200 if repo_new == repo_old else 201

                    result = response.json(repo_new, status=code)

            elif request.method == 'DELETE':
                if not repo.exists:
                    result = response.json(None, status=404)
                else:
                    repo.delete()
                    result = response.json(repo.dump())

            return result

        @self.app.route("/repos/<repo_name>/<scenario_name>", methods=['PUT', 'GET', 'DELETE', 'PATCH'])
        async def scenario_actions(request, repo_name, scenario_name):
            repo = Repository(self.db, name=repo_name)
            scenario = Scenario(self.db, name=scenario_name, repo_name=repo.name)

            if request.method == 'PUT':
                if len(request.body) < 4 or len(request.body) > 10240:
                    result = response.json('File size does not match sane limits', status=400)
                else:
                    code = 200 if scenario.exists else 201

                    scenario.name = scenario_name
                    scenario.repo = repo.name
                    scenario.data = request.body.decode()
                    scenario.save()

                    # FIXME
                    # This is unsafe, must load-append-save as a transaction here
                    repo.load()
                    if scenario.name not in repo.scenarios:
                        repo.scenarios.append(scenario.name)
                    repo.save()

                    result = response.json(scenario.dump(), status=code)

            elif request.method == 'GET':
                if not scenario.exists:
                    result = response.json(None, status=404)
                else:
                    result = response.json(scenario.dump())

            elif request.method == 'DELETE':
                if not scenario.exists:
                    result = response.json(None, status=404)
                else:
                    # FIXME
                    # This is unsafe, must load-remove-save as a transaction here
                    repo.load()
                    if scenario.name in repo.scenarios:
                        repo.scenarios.remove(scenario.name)
                    repo.save()

                    scenario.delete()

                    result = response.json(scenario.dump())

            elif request.method == 'PATCH':
                if not scenario.exists:
                    result = response.json(None, status=404)
                else:
                    job = Job(self.db, repo_name=repo.name, scenario_name=scenario.name)

                    await job.execute(scenario.data)

                    scenario.latest_job = job.name
                    scenario.save()

                    result = response.json(job.dump(), status=201)

            return result

        @self.app.route("/repos/<repo_name>/<scenario_name>/jobs/latest", methods=['GET'])
        async def scenario_job_latest(request, repo_name, scenario_name):
            repo = Repository(self.db, name=repo_name)
            scenario = Scenario(self.db, name=scenario_name, repo_name=repo.name)

            if not repo.exists:
                result = response.json('Repo not found', status=404)
            elif not scenario.exists:
                result = response.json('Scenario not found', status=404)
            else:
                if scenario.latest_job:
                    result = response.redirect('/jobs/' + scenario.latest_job)
                else:
                    result = response.json('No jobs found', status=404)

            return result

        @self.app.route("/jobs/<job_name>", methods=['GET', 'DELETE'])
        async def job_actions(request, job_name):
            job = Job(self.db)
            job.load(job_name)
            if request.method == 'GET':
                if job.state is None:
                    result = response.json(None, status=404)
                else:
                    result = response.json(job.dump())
            elif request.method == 'DELETE':
                if job.state is None:
                    result = response.json(None, status=404)
                else:
                    job.delete()
                    result = response.json(job.dump())

            return result

        @self.app.route("/webhooks/<repo_name>/<scenario_name>", methods=['POST'])
        async def webhooks(request, repo_name, scenario_name):
            is_github = 'X-GitHub-Event' in request.headers
            is_gitlab = 'X-Gitlab-Event' in request.headers

            pusher = request.json.get('pusher')

            if is_github or is_gitlab:
                event = request.headers['X-GitHub-Event'] or request.headers['X-Gitlab-Event']
                if not 'push' in event.lower() and not 'ping' in event.lower():
                    result = response.json('Got "{}", but accepts "push" and "ping" events only'.format(event), 501)

            if 'ping' in event.lower():
                result = response.json('Pong', 200)
            elif not pusher:
                result = response.json('Could not find "pusher" object in request JSON', 400)
            else:
                repo = Repository(self.db, name=repo_name)
                if not repo.exists:
                    result = response.json('Repo "{}" not found'.format(repo_name), 404)
                else:
                    scenario = Scenario(self.db, name=scenario_name, repo_name=repo.name)
                    if not scenario.exists:
                        result = response.json('Scenario "{}" not found'.format(repo_name), 404)
                    else:
                        job = Job(self.db)
                        job.repo = repo.name
                        job.scenario = scenario.name
                        job.load()
                        await job.execute(scenario.data, hook_data=request.json)
                        result = response.json(job.dump(), status=201)

            return result

    def run(self):
        self.app.run(
            host=self.app.config.API_HOST,
            port=self.app.config.API_PORT
        )
