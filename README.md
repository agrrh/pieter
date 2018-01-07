# Rationale

This is Pieter, a bear (yes, a bear) and a super-lightweight CI.

One day I realized that number of great tools doesn't suit one simple idea: **to provide lightweight private CI**

- [TeamCity](https://jetbrains.ru/products/teamcity/) and [Jenkins](https://jenkins-ci.org/) are way too heavy
- [Travis](https://travis-ci.org/) not suitable when one needs privacy
- [Drone](https://drone.io/) is container-oriented so sometimes an overhead

There are many other solutions, but it was hard to find one good enough to rapidly deploy and use in a minute or two. So meet the Pieter CI!

*Pieter pronounces more like St. Petersburg in short form, not like a person's name.*

# Key concepts

- **Lightweight**, daemon would never consume more than couple percents of your CPU
- **Compact**, tool designed to solve one and only issue: executing predefined jobs on demand
- **Easy**, absence of complex stuff and overmanagement makes deploy, learning and usage questions of minutes

# Requirements

- Python 3.5.2+
- API powered by [Sanic](https://github.com/channelcat/sanic)
- [Redis](https://redis.io/) as a database

# Installation

There are few ready-to-go ways to run the Pieter:

### Containers

#### Easy way

Containerized with [docker-compose](https://docs.docker.com/compose/)

```
docker-compose up
```

#### Flexible way

Run in containers isolated in private network:

```
docker network create pieter

docker run -d --name redis \
    -p 6379:6379 \
    --network pieter \
    -v $(pwd)/data:/data \
    redis

docker run -d --name pieter-ci \
    -p 8000:8000 \
    --network pieter \
    agrrh/pieter-ci:stable
```

You could also customize env variables pointing API on which address/port to listen and where to seek for DB, these are defaults:

```
PIETER_DB_HOST=redis
PIETER_DB_PORT=6379
PIETER_API_HOST=0.0.0.0
PIETER_API_PORT=8000
```

### Manual

Run locally for test purposes, development or containers-free setup:

```
# First, run redis in your way of choice

# source local.env
export PIETER_DB_HOST=127.0.0.1
export PIETER_DB_PORT=6379
export PIETER_API_HOST=127.0.0.1
export PIETER_API_PORT=8000

./pieter

http http://127.0.0.1:8000/
```

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
