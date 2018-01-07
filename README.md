# Installation

There are two main ways to run the app.

Containerized with [docker-compose](https://docs.docker.com/compose/):

```
docker-compose up
```

Run locally for test purposes, development or containers-free setup:

```
docker run -d -p 6379:6379 -v $(pwd)/data:/data redis

# source local.env
export PIETER_DB_HOST=127.0.0.1
export PIETER_DB_PORT=6379
export PIETER_API_HOST=127.0.0.1
export PIETER_API_PORT=8000

./pieter

http http://127.0.0.1:8000/
```

# Requirements

- Python 3.5.2+
- API powered by [Sanic](https://github.com/channelcat/sanic)
- [Redis](https://redis.io/) as a database

All required libraries could be installed with:

```
pip3 install -r requirements.txt
```

# API examples

Those examples are using awesome [httpie](https://httpie.org/).

Get repos list:

`http GET http://0.0.0.0:8000/repos`

### Repo lifecycle

Create:

`http PUT http://0.0.0.0:8000/repos/pieter source=git@github.com:agrrh/pieter-ci.git`

Examine:

`http GET http://0.0.0.0:8000/repos/pieter`

Remove (wait, don't run it yet):

`http DELETE http://0.0.0.0:8000/repos/pieter`

### Scenario lifecycle

Add new scenario (aka build):

`http PUT http://0.0.0.0:8000/repos/pieter/build.sh < misc/test_script.sh`

Check it contents:

`http GET http://0.0.0.0:8000/repos/pieter/build.sh`

Remove scenario (same, don't run it now):

`http DELETE http://0.0.0.0:8000/repos/pieter/build.sh`

### Job lifecycle

Run a job:

`http PATCH http://0.0.0.0:8000/repos/pieter/build.sh`

Check job status:

`http GET http://0.0.0.0:8000/jobs/${JOB_ID}`

Delete job info and artifacts:

`http DELETE http://0.0.0.0:8000/jobs/${JOB_ID}`

### Cleanup

Now feel free to delete test repo and everything:

```
http DELETE http://0.0.0.0:8000/repos/pieter
# also removes child scenarios

http DELETE http://0.0.0.0:8000/jobs/${JOB_ID}
```
