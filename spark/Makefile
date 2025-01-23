# Makefile for Dockerized Apache Spark Cluster

build:
	docker compose build

build-nc:
	docker compose build --no-cache

build-progress:
	docker compose build --no-cache --progress=plain

down:
	docker compose down --volumes

run-recreate:
	make down && docker compose up -d --force-recreate

run-scaled:
	make down && docker compose up --scale spark-worker=3

run-d:
	make down && docker compose up -d

stop:
	docker-compose stop

submit:
	docker exec spark-master-container spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)

submit-delta:
	docker exec spark-master-container spark-submit --packages io.delta:delta-spark_2.12:3.3.0 --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)