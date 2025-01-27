from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from custom_hook import CustomAPIHook

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

def fetch_and_transfer_data(**kwargs):
    hook = CustomAPIHook(conn_id='my_custom_api')
    
    # Fetch data from source
    source_data = hook.get_data(endpoint='source_endpoint')

    # Optionally transform data here
    # transformed_data = transform(source_data)
    transformed_data = source_data  # Example without transformation

    # Write data to destination
    hook.write_data(data=transformed_data, endpoint='destination_endpoint')

with DAG(dag_id='custom_data_transfer', default_args=default_args, schedule_interval='@daily') as dag:
    fetch_transfer_task = PythonOperator(
        task_id='fetch_and_transfer',
        python_callable=fetch_and_transfer_data,
        provide_context=True
    )
