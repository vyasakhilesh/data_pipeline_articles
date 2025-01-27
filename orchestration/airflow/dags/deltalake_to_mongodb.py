from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'testuser',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

def extract_transform_load(delta_table_path, mongo_uri, mongo_db, mongo_collection):
    from pyspark.sql import SparkSession
    from pymongo import MongoClient
    from delta.tables import DeltaTable
    from airflow.models import Variable
    last_load_timestamp = Variable.get("last_load_timestamp", default_var=None)

    spark = SparkSession.builder \
        .appName("Delta to MongoDB") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    delta_table = DeltaTable.forPath(spark, delta_table_path)

    if last_load_timestamp:
        # Load only new or updated data since the last load timestamp
         df = delta_table.toDF().filter(f"modificationTime > '{last_load_timestamp}'")
    else:
        # Load all data if no last load timestamp is found
        df = delta_table.toDF()

     # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Convert DataFrame to dictionary and insert into MongoDB
    records = df.toPandas().to_dict('records')
    collection.insert_many(records)

    # Update the last load timestamp to the current time
    current_time = datetime.utcnow().isoformat()
    Variable.set("last_load_timestamp", current_time)
     # Close the MongoDB connection
    client.close()

    # Stop the Spark session
    spark.stop()

dag = DAG(dag_id='delta_to_mongodb_incremental', default_args=default_args, schedule_interval=None)
start = DummyOperator(task_id='start')
extract_transform_load = PythonVirtualenvOperator(
    task_id='extract_transform_load',
    python_callable=extract_transform_load,
    op_kwargs={
            'delta_table_path': "/opt/spark/data/delta_table/core_data",
            'mongo_uri': "mongodb://mongoadmin:password@localhost:27017",
            'mongo_db': "test_db",
            'mongo_collection': "test_collection"
        },
    requirements=['delta-spark', 'pyspark', 'pymongo'],
    system_site_packages=True,
    python_version='3.10',
    dag=dag
)
end = DummyOperator(task_id='end')

start >> extract_transform_load  >> end