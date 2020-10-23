service=user-service
worker=app
partitions=4

build:
	docker-compose build

restart:
	docker-compose restart ${service}

run:
	docker-compose up

logs:
	docker-compose logs

remove:
	docker-compose rm -svf

stop:
	docker-compose stop

lint:
	python3 -m pylint faust_app/faustapp

dev:
	docker-compose up --detach --build faust

run-dev: build run

clean: stop remove

