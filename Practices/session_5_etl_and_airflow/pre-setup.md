# PRE SETUP

## Prerequisites

* [Docker][install_docker]

## Steps

### Step 1 - Composer

* Run the docker-compose.yml that start docker containers that has Airflow Celery Components

  ```sh
  docker-compose up -d
  ```

### Step 2 -  Airflow Web UI

Once docker-compose runs all the Airflow Celery component containers

* Open a web browser and open following URL to access to Airflow Web UI:
  * <http://localhost:8080>
  ![img](documentation_images/airflow-2.png)

* Login
  * username: `airflow`
  * password: `airflow`

  ![img](documentation_images/airflow-3.png)

* Example DAG's

  ![img](documentation_images/airflow-4.png)

### Step 3 (Optional) - Install VSCode Extension

This extension will decode the `parquet` files into a json, so you can visualize them

* Open `VSCode`
* Go to `Extensions`
* Search `dvirtz.parquet-viewer`
* Click Install

  >Wait for the installation to be completed

## Links

* [Install Docker][install_docker]

[install_docker]: https://docs.docker.com/engine/install/
