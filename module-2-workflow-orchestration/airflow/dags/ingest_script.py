from time import time
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def ingest_callable(user, password, host, port, db, table_name, file, **context):
    print("Starting ingest_callable", flush=True)

    execution_date = context.get('data_interval_start')
    print(table_name, file, execution_date, user, password, flush=True)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    conn = engine.connect()

    print('Connection established successfully, inserting data...')

    t_start = time()

    parquet_file = pq.ParquetFile(file)
    batch_size = 10000
    first_batch = True
    total_rows = 0

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df = pd.DataFrame(batch.to_pandas())

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        if first_batch:
            # Create the table with correct schema
            df.head(0).to_sql(name=table_name, con=conn, if_exists='replace')
            first_batch = False

        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        total_rows += len(df)
        print(f"Inserted {total_rows} rows...", flush=True)

    t_end = time()
    print(f'Inserted total {total_rows} rows, took {t_end - t_start:.2f} seconds')

    conn.close()