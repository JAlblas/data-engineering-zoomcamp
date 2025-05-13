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
