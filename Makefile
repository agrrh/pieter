branch := $(shell git rev-parse --abbrev-ref HEAD)

clean:
	bash misc/cleanup_jobs_dir.sh

tests: clean
	test "$(branch)" = "master" && nosetests -v; true

build: tests
	docker build -t agrrh/pieter-ci:$(branch) .

publish: build
	docker push agrrh/pieter-ci:$(branch)
	test "$(branch)" = "master" && docker push agrrh/pieter-ci; true
