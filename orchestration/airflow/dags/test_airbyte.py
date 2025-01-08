from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def your_task_function():
    import airbyte as ab

    source = ab.get_source(
        "source-faker",
        config={"count": 5_000},
        install_if_missing=True,
    )
    source.check()
    source.select_all_streams()
    result = source.read()

    for name, records in result.streams.items():
        print(f"Stream {name}: {len(list(records))} records")

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2025, 1, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('task_dependency_airbyte_dag', default_args=default_args, schedule_interval='@daily')

start = DummyOperator(task_id='start')
sources_caches = PythonVirtualenvOperator(
    task_id='test_sources_caches',
    python_callable=your_task_function,
    requirements=['setuptools','wheel', 'pendulum','airbyte'],
    system_site_packages=False,
    python_version='3.12',
    dag=dag,
)
end = DummyOperator(task_id='end')

start >> sources_caches >> end