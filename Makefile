clean:
	bash misc/cleanup_jobs_dir.sh

tests: clean
	nosetests -v

build: clean
	docker build -t agrrh/pieter-ci:dev .

build-stable: clean
	docker build -t agrrh/pieter-ci:stable .

publish: build
	docker push agrrh/pieter-ci:dev

publish-stable: build-stable
	docker push agrrh/pieter-ci:stable
	docker push agrrh/pieter-ci
