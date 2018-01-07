clean:
	bash misc/cleanup_jobs_dir.sh

tests: clean
	nosetests -v

build: clean
	docker build -t agrrh/pieter-ci:dev .

publish: clean build
	docker push agrrh/pieter-ci:dev
	docker push agrrh/pieter-ci
