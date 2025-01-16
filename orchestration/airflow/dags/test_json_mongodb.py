from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

def json_to_mongodb():
    print("################################ YOUR TASK FUNCTION ################################")
    import airbyte as ab
    import os
    import stat
    from pathlib import Path

    # Create and configure the source:
    source = ab.get_source(
        "source-github",
        install_if_missing=True,
        config={
            "repositories": ["vyasakhilesh/data_pipeline_articles"],
            "credentials": {
                "personal_access_token": GITHUB_PERSONAL_ACCESS_TOKEN,
            },
        },
        # local_executable=Path('/opt/airflow/venvs/.venv-source-github/bin/'),
        # install_root=Path('/opt/airflow/venvs'),
    )

    # Verify the config and creds by running `check`:
    print (source.check())

default_args = {
    'owner': 'testuser',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('github_airbyte_dag', default_args=default_args, schedule_interval=None)

start = DummyOperator(task_id='start')
pre_cleanup_task = BashOperator( task_id='pre_cleanup_virtualenv', bash_command='rm -rf /opt/***/.venv-source-github', dag=dag, )
sources_caches = PythonVirtualenvOperator(
    task_id='test_sources_caches',
    python_callable=your_task_function,
    requirements=['airbyte==0.22.0'],
    system_site_packages=True,
    python_version='3.10',
    dag=dag
)
post_cleanup_task = BashOperator( task_id='post_cleanup_virtualenv', bash_command='rm -rf /opt/***/.venv-source-github', dag=dag, )
end = DummyOperator(task_id='end')

start >> pre_cleanup_task >> sources_caches >> post_cleanup_task >> end

