# Notes Module 1

The different "systems" of a ETL/ELT process can be run from seperate Docker containers, for example a pipeline running on Ubuntu, Postgres & pgAdmin:

![image](img/containers.png)

Running an ETL (Extract, Transform, Load) script within a Docker container is best practice in many real-world data engineering and DevOps workflows. Here's why:

## Why use containers:

- Isolation: Docker ensures the ETL script runs in a clean, isolated environment with all its dependencies (Python version, libraries, credentials, etc.), avoiding "it works on my machine" issues.

- Portability: Once your ETL is containerized, you can run it consistently across different environments (development, testing, production) without worrying about system differences. It is easy to deploy to the cloud as well.

- Reproducibility: You can version control your Dockerfile and ETL code together, so the exact setup can be reproduced or rolled back.

- Scalability: In production environments, containers can be orchestrated (e.g., using Kubernetes or Docker Compose) to run ETL jobs on a schedule or in response to events.

- Local Experiments: Docker helps with local experiments by making it easy to quickly spin up environments: You can try out new tools, versions, or configurations without polluting your system. E.g., test a Python script on Python 3.7 while your system has Python 3.12. Need to test your app with a PostgreSQL database? Just run a PostgreSQL container.

- Integration Tests: Docker supports integration testing by:

  - Spinning up dependencies: Use Docker Compose to run your app alongside databases, message queues, etc.
  - Running tests in CI/CD: The same containers used locally can run in GitHub Actions, GitLab CI, etc., ensuring environment parity.
  - Clean state: Each test run can start fresh, preventing test pollution.
  - Parallel execution: You can run isolated test environments in parallel using separate containers.

## Docker Basics

Running a container:

    docker run <container name>

Running a container in interactive mode with tag and bash parameter:

    docker run -it <container name>:<tag> bash

Building an image in this directory\_

    docker build -t <image name> .

## Creating our own Dockerfile:

You might have a Dockerfile like this:

    FROM python:3.10

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt

    COPY . .

    CMD ["python", "etl_script.py"]

Then build and run it:

    docker build -t my-etl-job .
    docker run my-etl-job

## Running a postgres container

This is the command used in the postgres video to startup a docker container running postgres.

    docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13

It is important to set the environmental variables by inputting them with the -e flag.

- **docker run -it** Runs an interactive (-it) container so you can see logs and interact with it in the terminal.

- **-e POSTGRES_USER="root"** Sets the username for the database superuser to "root".

- **-e POSTGRES_PASSWORD="root"** Sets the password for the "root" user.

- **-e POSTGRES_DB="ny_taxi"** Creates a new database called ny_taxi on startup.

- **-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data**
  Mounts a volume from your current directory (ny_taxi_postgres_data) to the container's PostgreSQL data directory, enabling data persistence.

- **-p 5432:5432** Forwards port 5432 on your machine to port 5432 in the container so you can access PostgreSQL from outside the container (e.g., with DBeaver, pgAdmin, or a script).

- **postgres:13** Specifies the Docker image to use: PostgreSQL version 13.

#### Remember not to put the /ny_taxi_postgres_data folder in your git!

## Using pgcli to access the postgres database

First install the pgcli package if needed:

    pip install pgcli

Then run it to connect to the postgres database running in the container:

    pgcli -h localhost -p 5432 -u root -d ny_taxi

This shows us that a connection is working. You can list tables by running:

    \dt

but unfortunately we have have no data or tables to look at. Let's work on that!

## Using Jupyter Notebook to ingest data

Here we learn how to use Jupyter Notebook to look at the data and we ingest data with the use of the pandas library.

We can start Jupyter Notebook with the following command:

    jupyter notebook

    # if jupyter is not installed run pip install jupyter

We now download the taxi data:

    wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

We can read this file with the read_csv pandas function:

    df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)

To change panda columns to datetime we can parse them by running:

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

Now we need to get the schema (DDL statement) by running:

    print(pd.io.sql.get_schema(df, name="yellow-taxi-data"))

    CREATE TABLE "yellow-taxi-data" (
        "VendorID" INTEGER,
        "tpep_pickup_datetime" TIMESTAMP,
        "tpep_dropoff_datetime" TIMESTAMP,
        "passenger_count" INTEGER,
        "trip_distance" REAL,
        "RatecodeID" INTEGER,
        "store_and_fwd_flag" TEXT,
        "PULocationID" INTEGER,
        "DOLocationID" INTEGER,
        "payment_type" INTEGER,
        "fare_amount" REAL,
        "extra" REAL,
        "mta_tax" REAL,
        "tip_amount" REAL,
        "tolls_amount" REAL,
        "improvement_surcharge" REAL,
        "total_amount" REAL,
        "congestion_surcharge" REAL
    )

Pandas uses a library called SQLAlchemy to communicate with SQL databases. We can import this by running:

    from sqlalchemy import create_engine

Then we can create a engine object:

    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

This gave me the following error:
ModuleNotFoundError: No module named 'psycopg2
which we can solved by running:

    pip install psycopg2-binary

We can test the connect by running:

    engine.connect()

Now we can use the engine variable to add inside of the pd.io.sql.get_schema call to get the correct format for our type of database:

    print(pd.io.sql.get_schema(df, name="yellow-taxi-data", con=engine))

We can now create an iterator to :

    df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

Now we can keep reading from the dataset until an exception gets thrown. Not the most elegant way to do this but it works!

    from time import time

    while True:
        t_start = time()

        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

        t_end = time()

        print('Inserted another chunk. It took %.3f second ' % (t_end - t_start))

If you feel this was a bit to dirty, you can add a try catch block:

    while True:
        t_start = time()

        try:
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

            t_end = time()

            print('Inserted another chunk. It took %.3f second ' % (t_end - t_start))

        except StopIteration:
            print("No more data to process.")
            break
        except Exception as e:
            print("An error occurred:", e)
            break

## Time to use pgadmin instead of pgcli

pgcli is great and all, but working in the command prompt can be a bit tedious. If you prefer working within a GUI then pgadmin is a great choice! We can start up a docker container running pgadmin4 like this:

    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        dpage/pgadmin4

Unfortunately, we cannot connect to the postgres container from the pgadmin container. If we try connecting to the postgres database from pgadmin using localhost as host name we get an error! This is because localhost means that pgadmin tries to look for the database on its own container.

To be able to connect it we need to link the two containers. We can use this by using a docker network. We need to close both running contains and create a new docker network by running:

    docker network create pg-network

Now we need to start up both containers again, with the added flags called --network and --name. Network provides the network name to connect to, and name is the name used as hostname for the container.

    docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name=pg-database \
    postgres:13

And the samae for pgadmin:

    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        --network=pg-network \
        --name=pg-database \
        dpage/pgadmin4

Now create the connection to the postgres database in pgadmin with pg-database as the hostname. You should be able to connect now.
Pretty awesome right? Well, yes but still quite tedious, but luckily there is a solution to this, Docker compose! But more on that a bit later.

## Dockerizing our ingestion script

In this video we refactor our jupyter notebook file to a regular python script using the following command:

    jupyter nbconvert --to=script upload-data.ipynb

We then continue using argparse to make the script dynamic by enabling us to enter command line arguments through the use of docker run environmental variables. The finished code looks like this:

    #!/usr/bin/env python
    # coding: utf-8

    from time import time
    from sqlalchemy import create_engine
    import pandas as pd
    import argparse
    import os

    def main(params):
        user = params.user
        password = params.password
        host = params.host
        port = params.port
        db = params.db
        table_name = params.table_name
        url = params.url
        csv_name = 'output.csv'

        # download the CSV file
        os.system(f"wget {url} -O {csv_name}")

        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip')

        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        df.to_sql(name=table_name, con=engine, if_exists='append')

        while True:
            t_start = time()

            try:
                df = next(df_iter)

                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

                df.to_sql(name=table_name, con=engine, if_exists='append')

                t_end = time()

                print('Inserted another chunk. It took %.3f second ' % (t_end - t_start))

            except StopIteration:
                print("No more data to process.")
                break
            except Exception as e:
                print("An error occurred:", e)
                break

    if __name__ == '__main__':
        # Parse the command line arguments and calls the main program
        parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

        parser.add_argument('--user', help='user name for postgres')
        parser.add_argument('--password', help='password for postgres')
        parser.add_argument('--host', help='host for postgres')
        parser.add_argument('--port', help='port for postgres')
        parser.add_argument('--db', help='database name for postgres')
        parser.add_argument('--table_name', help='name of the table where we will write the results to')
        parser.add_argument('--url', help='url of the csv file')

        args = parser.parse_args()

        main(args)

Note that the create_engine now uses the parsed arguments to create the connection string.

Note that the file download is currently is:
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

We can run the python script like so:

    python ingest_data.py \
        --user=root \
        --password=root \
        --host=localhost \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

## Docker compose
