import os

from time import time

import pandas as pd
from sqlalchemy import create_engine


def ingest_callable(user, password, host, port, db, table_name, csv_file,  **context):
    print("Starting ingest_callable", flush=True)

    execution_date = context.get('data_interval_start')
    print(table_name, csv_file, execution_date, user, password, flush=True)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print('connection established successfully, inserting data...')

    t_start = time()
    df = pd.read_parquet(csv_file)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    t_end = time()
    print('inserted data, took %.3f second' % (t_end - t_start))