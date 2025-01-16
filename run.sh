docker-compose up -d --build
docker compose up -d --force-recreate
cd ./orchestration/airflow
sudo chown -R 50000:0 venvs
