# Rationale

This is Pieter, a bear (yes, a bear) and a super-lightweight CI.

One day you could realize that number of great tools doesn't fully suit simple idea: to provide lightweight private CI.

- [TeamCity](https://jetbrains.ru/products/teamcity/) and [Jenkins](https://jenkins-ci.org/) are way too heavy
- [Travis](https://travis-ci.org/) not suitable when one needs privacy
- [Drone](https://drone.io/) is container-oriented so sometimes an overhead
- ...

There are many other solutions, but it was hard to find one good enough to rapidly deploy and use in a minute or two.

So meet the Pieter CI!

*Pieter pronounces more like St. Petersburg in short form, not like a person's name.*

# Key concepts

- **Lightweight**, daemon would never consume more than couple percents of your CPU
- **Compact**, tool designed to solve one and only issue: executing predefined jobs on demand
- **Easy**, absence of complex stuff and overmanagement makes deploy, learning and usage questions of minutes

# Requirements

- [Python](https://www.python.org/) 3.5.2+
- API powered by [Sanic](https://github.com/channelcat/sanic)
- [Redis](https://redis.io/) as a database

# Installation

Some ways to run Pieter CI:

### Containers

#### Easy way

Using [docker-compose](https://docs.docker.com/compose/):

```
docker-compose up
```

#### Flexible way

Run as standalone containers isolated in private network:

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

### Manual way

Run locally for test purposes, development or containers-free setup:

```
# First, run redis in your way of choice

source misc/local.env
./pieter

http http://127.0.0.1:8000/
```

All required libraries could be installed with:

```
pip3 install -r requirements.txt
```

# Configuraion

You could customize env variables pointing API on which address/port to listen and where to seek for DB, these are defaults:

```
PIETER_DB_HOST=redis
PIETER_DB_PORT=6379
PIETER_API_HOST=0.0.0.0
PIETER_API_PORT=8000
PIETER_API_PREFIX=""
```

# API examples

Those examples are using awesome [httpie](https://httpie.org/).

### Repo lifecycle

Repository is an object you want to interact with.

This could be code repository to build application from or just a webpage to download on specific events.

##### List repositories

`http GET http://0.0.0.0:8000/repos`

##### Create repository

`http PUT http://0.0.0.0:8000/repos/pieter source=git@github.com:agrrh/pieter-ci.git`

##### Examine repo

`http GET http://0.0.0.0:8000/repos/pieter`

##### Remove repo

`http DELETE http://0.0.0.0:8000/repos/pieter`

### Scenario lifecycle

Scenario is some item related to "build" object. Set of rules which would be applied to repository when requested.

##### Add scenario

`http PUT http://0.0.0.0:8000/repos/pieter/build.sh < misc/test_script.sh`

##### View scenario

`http GET http://0.0.0.0:8000/repos/pieter/build.sh`

##### Remove scenario

`http DELETE http://0.0.0.0:8000/repos/pieter/build.sh`

### Job lifecycle

##### Run a job

`http PATCH http://0.0.0.0:8000/repos/pieter/build.sh`

##### Check job status

`http GET http://0.0.0.0:8000/jobs/${JOB_ID}`

##### Delete a job

`http DELETE http://0.0.0.0:8000/jobs/${JOB_ID}`

# Credits

- [Kirill K](https://github.com/agrrh) - author
