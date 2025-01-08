# Steps

1. Create folders and directories
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

2. Download  docker-compose.yml flie and comment
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
```
```yml
#image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.10.4}
build: .
```
```bash
docker compose up -d --force-recreate
```