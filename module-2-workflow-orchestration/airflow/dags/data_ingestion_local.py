import os
from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script import ingest_callable, upload_to_gcs

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data' 
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{ data_interval_start.strftime(\'%Y-%m\') }}.parquet'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ data_interval_start.strftime(\'%Y-%m\') }}.parquet'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ data_interval_start.strftime(\'%Y_%m\') }}'
GCS_PATH = 'raw/yellow_tripdata/{{ data_interval_start.strftime(\'%Y\') }}/yellow_tripdata_{{ data_interval_start.strftime(\'%Y-%m\') }}.parquet'

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

local_workflow = DAG(
    "LocalIngestionDAG",
    schedule="0 6 2 * *",
    start_date=datetime(2019, 1, 1),
    catchup=True
)

with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
         bash_command=f'curl -sSLf {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
    )

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            file=OUTPUT_FILE_TEMPLATE
        ),
    )

    local_to_gcs_task = PythonOperator(
        task_id="upload_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": GCS_PATH,
            "local_file": OUTPUT_FILE_TEMPLATE,
        },
    )

    '''
    rm_task = BashOperator(
        task_id="rm_task",
        bash_command=f"rm {local_csv_path_template} {local_parquet_path_template}"
    )
    '''
    

    wget_task >> ingest_task >> local_to_gcs_task # >> rm_task