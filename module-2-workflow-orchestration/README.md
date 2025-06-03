# Notes Module 2

This lesson provides an in-depth exploration of Data Lakes and the orchestration of data pipelines using Apache Airflow. Understanding these concepts is crucial for managing and processing large volumes of data efficiently.

## Data Lake

A Data Lake is a centralized repository designed to store vast amounts of raw data in various formats, including structured, semi-structured, and unstructured data. The primary goal of a Data Lake is to ingest data quickly and make it accessible to team members for analysis and processing.

### Key Characteristics of a Data Lake

- **Security:** Ensuring that data is protected and accessible only to authorized users.
- **Scalability:** The ability to scale storage and processing capabilities as data volumes grow.
- **Cost-Effectiveness:** Running on inexpensive hardware to keep costs low.

### Data Lake vs. Data Warehouse

Understanding the differences between a Data Lake and a Data Warehouse is essential for choosing the right storage solution for your data needs.

| Aspect              | Data Lake (DL)                                                                                                                 | Data Warehouse (DW)                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Processing** | Stores raw data with minimal processing. The data is generally unstructured and can be used for a wide variety of purposes.    | Stores refined data that has been cleaned, pre-processed, and structured for specific use cases, such as business intelligence and reporting. |
| **Size**            | Large, often in the order of petabytes. Data is transformed only when it is used and can be stored indefinitely.               | Smaller in comparison. Data is always preprocessed before ingestion and may be purged periodically to manage storage costs.                   |
| **Nature**          | Data is undefined and versatile, making it suitable for various analytical and machine learning tasks.                         | Data is historical and relational, often used for transaction systems and structured queries.                                                 |
| **Users**           | Primarily used by data scientists and data analysts who need access to raw data for exploratory analysis and machine learning. | Used by business analysts who require structured data for reporting and business intelligence.                                                |
| **Use Cases**       | Ideal for stream processing, machine learning, and real-time analytics where raw data is needed.                               | Suited for batch processing, business intelligence, and reporting where structured and processed data is required.                            |

Data Lakes emerged as companies realized the importance of collecting data even before it could be ingested into a Data Warehouse. This ensured that no potentially useful data was lost during the development of necessary relationships and schemas for a Data Warehouse.

### ETL vs. ELT

The process of ingesting data into a Data Lake or Data Warehouse involves different approaches:

- **ETL (Extract, Transform, Load):** Used in Data Warehouses, where data is transformed (cleaned, pre-processed, etc.) before it is loaded into the warehouse. This approach is often referred to as "Schema on Write."
- **ELT (Extract, Load, Transform):** Used in Data Lakes, where data is loaded directly into the lake without any transformations. Any necessary schemas are derived when the data is read from the Data Lake. This approach is known as "Schema on Read."

### Data Swamp

A Data Lake can degenerate into a Data Swamp if not properly managed. A Data Swamp is characterized by:

- Lack of versioning, making it difficult to track changes and maintain data integrity.
- Incompatible schemas for the same data, leading to inconsistencies and errors.
- Missing metadata, making it challenging to understand and use the data effectively.
- Inability to join datasets, limiting the potential for comprehensive analysis.

To prevent a Data Lake from becoming a Data Swamp, it is essential to implement proper data management practices, including versioning, metadata management, and schema compatibility.

### Data Lake Cloud Providers

Several cloud providers offer Data Lake solutions, including:

- **Google Cloud Platform:** Cloud Storage
- **Amazon Web Services:** Amazon S3
- **Microsoft Azure:** Azure Blob Storage

## Orchestration with Airflow

### Introduction to Workflow Orchestration

Workflow orchestration involves managing and coordinating multiple tasks in a data pipeline. Apache Airflow is a powerful tool for defining, scheduling, and monitoring workflows, making it easier to manage complex data pipelines.

### Airflow Architecture

A typical Airflow installation consists of several components:

- **Scheduler:** Handles triggering scheduled workflows and submitting tasks to the executor. The scheduler is the core component of Airflow, responsible for managing task execution.
- **Executor:** Runs tasks either locally or on workers. In a default installation, the executor runs everything inside the scheduler, but production-suitable executors push task execution out to workers.
- **Worker:** Executes tasks given by the scheduler. Workers are essential for scaling task execution across multiple machines.
- **Webserver:** Provides a graphical user interface (GUI) for managing and monitoring workflows.
- **DAG Directory:** A folder containing DAG files that are read by the scheduler and executor. This directory is crucial for defining and managing workflows.
- **Metadata Database:** Stores state information used by the scheduler, executor, and webserver. This database is the backend of Airflow, storing information about task instances, DAG runs, and more.
- **Additional Components:**
  - **Redis:** A message broker that forwards messages from the scheduler to workers.
  - **Flower:** An application for monitoring the environment, typically available at port 5555 by default.
  - **airflow-init:** An initialization service that can be customized for specific needs.

### Setting Up Airflow with Docker

Setting up Airflow with Docker involves several steps to ensure a smooth and efficient deployment.

#### Prerequisites

- Ensure that `docker-compose` is at least version v2.x+ and that Docker Engine has at least 5GB of RAM available, ideally 8GB. This can be configured in Docker Desktop under Preferences > Resources.
- Ensure that the service account credentials JSON file is named `google_credentials.json` and stored in `$HOME/.google/credentials/`.

#### Setup (Full Version)

1. **Create a New Airflow Subdirectory:** Start by creating a new subdirectory in your work directory for Airflow.

2. **Download the Docker-compose YAML File:** Download the official Docker-compose YAML file for the latest Airflow version using the following command:
   ```bash
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'
   ```
