branch := $(shell git rev-parse --abbrev-ref HEAD)

port_num := $(shell echo -n $(branch) | cksum | cut -c 1-3)
branch_hash := $(shell echo 6$(port_num))

clean:
	bash misc/cleanup_jobs_dir.sh

start: build
	docker network create pieter_$(branch)
	docker run -d --name redis_pieter_$(branch) --network pieter_$(branch) redis:3-alpine
	docker run -d --name pieter_$(branch) --network pieter_$(branch) -e PIETER_DB_HOST=redis_pieter_$(branch) -p 8000:8000 agrrh/pieter-ci:$(branch)

stop:
	docker rm -f redis_pieter_$(branch)
	docker rm -f pieter_$(branch)
	docker network rm pieter_$(branch)

tests: clean
	nosetests -v

tests_api: clean
	nosetests -v tests/test_50_api.py

build: clean
	docker build -t agrrh/pieter-ci:$(branch) .

publish: start tests_api stop
	docker push agrrh/pieter-ci:$(branch)
	test "$(branch)" = "master" && docker push agrrh/pieter-ci; true
