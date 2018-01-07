```
# get repos
http GET http://0.0.0.0:8000/repos

# repo lifecycle
http PUT http://0.0.0.0:8000/repos/pieter source=git@github.com:agrrh/pieter-ci.git
http GET http://0.0.0.0:8000/repos/pieter
http DELETE http://0.0.0.0:8000/repos/pieter

# scenario lifecycle
http PUT http://0.0.0.0:8000/repos/pieter/build.sh < ~/bin/timestamp
http GET http://0.0.0.0:8000/repos/pieter/build.sh
http DELETE http://0.0.0.0:8000/repos/pieter/build.sh

# job lifecycle
http PATCH http://0.0.0.0:8000/repos/pieter/build.sh
http GET http://0.0.0.0:8000/jobs/${JOB_ID}
http DELETE http://0.0.0.0:8000/jobs/${JOB_ID}
```
