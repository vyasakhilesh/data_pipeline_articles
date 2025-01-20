from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'testuser',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('el_airbyte_dag', default_args=default_args, schedule_interval=None)

def json_to_mongodb():
    print("################################ YOUR TASK FUNCTION ################################")
    import airbyte as ab
    import os
    import stat
    from pathlib import Path

    # Create and configure the source:
    # connector_list = ab.get_available_connectors()
    # print (connector_list)
    
    # setup source for airbyte
    source = ab.get_source(
    "source-file",
    install_if_missing=True,)
    print(source.check())
    
    # Destination - destination-mongodb
    # destination-local-json
    # destination-qdrant


start = DummyOperator(task_id='start')
pre_cleanup_task = BashOperator( task_id='pre_cleanup_virtualenv', bash_command='rm -rf /opt/***/.venv-source-github', dag=dag, )
el_task = PythonVirtualenvOperator(
    task_id='test_el_task',
    python_callable=json_to_mongodb,
    requirements=['airbyte==0.22.0'],
    system_site_packages=True,
    python_version='3.10',
    dag=dag
)
post_cleanup_task = BashOperator( task_id='post_cleanup_virtualenv', bash_command='rm -rf /opt/***/.venv-source-github', dag=dag, )
end = DummyOperator(task_id='end')

start >> pre_cleanup_task >> el_task >> post_cleanup_task >> end

