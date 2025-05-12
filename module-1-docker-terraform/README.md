# Notes Module 1

The different "systems" of a ETL/ELT process can be run from seperate Docker containers, for example a pipeline running on Ubuntu, Postgres & pgAdmin:

![image](img/containers.png)

Running an ETL (Extract, Transform, Load) script within a Docker container is best practice in many real-world data engineering and DevOps workflows. Here's why:

## Why it makes sense:

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

## Example Dockerfile:

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
