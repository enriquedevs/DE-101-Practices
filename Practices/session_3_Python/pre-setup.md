# Pre-setup

## Steps

### Step 1 - Docker Compose

![img](img/docker-compose.png)

* Create a `docker-compose.yml` file with the following content

  ```yml
  version: '3'
  services:
    postgres_db:
      image: postgres:11.1
      environment:
        POSTGRES_PASSWORD: mypassword
        POSTGRES_DB: animaldb
        POSTGRES_USER: myuser
      ports:
        - 5433:5432
      networks:
        - app-tier
      volumes:
        - ./postgres:/docker-entrypoint-initdb.d

    python_app:
      build:
        context: .
        dockerfile: Dockerfile
      depends_on:
        - postgres_db
      networks:
        - app-tier
      command:
        tail -f /dev/null
      environment:
        POSTGRE_HOST: postgres_db
        POSTGRE_PORT: 5432
        POSTGRE_DB: animaldb
        POSTGRE_USER: myuser
        POSTGRE_PASSWORD: mypassword

  networks:
    app-tier:
      driver: bridge
  ```

  * The first line specifies the version of the Docker Compose file format.
  * Under `services`, two services are defined: `postgres_db` and `python_app`.
  * The `postgres_db` service uses the `postgres:11.1` image, which is a version of the official PostgreSQL image from Docker Hub with version 11.1.
    It has an environment variable block, which sets the values for the POSTGRES_PASSWORD, POSTGRES_DB and POSTGRES_USER environment variables.
  * The ports block maps the container's port `5432` to the host's port `5433`, allowing external connections to the PostgreSQL service.
  * The `networks` block links the container to the `app-tier` network.
  * The `volumes` block creates a mount point to the host's `./postgres` directory and maps it to `/docker-entrypoint-initdb.d` directory in the container. This allows any files in the `./postgres` directory on the host to be accessible inside the container.

    ![img](img/docker-volume.png)

  * The `python_app` service is configured to build the container using the "Dockerfile" in the current directory and the context is set to the current directory (.)
  * `depends_on` block is used to specify that the `python_app` container should be started after the `postgres_db` container.
  * `networks` block links the container to the `app-tier` network.
  * `command` block is used to specify a command that should be run when the container starts. Here is it runs `tail -f /dev/null` command.
  * Under `networks`, the app-tier network is defined using the bridge driver. This network allows containers to communicate with each other using their hostnames.
    ![img](img/docker-network.png)

>Overall, this file creates two services, postgres_db and python_app. postgres_db service runs postgres:11.1 image and python_app service runs an image built from a Dockerfile in the current directory. These services are connected to the same network and python_app is dependent on postgres_db service.

### Step 2 - Dockerfile

* Create a Dockerfile for `python_app`

  ```Dockerfile
  # Use the official Python 3.10 image as the base image
  FROM python:3.10

  # Set the working directory in the container
  WORKDIR /app

  # Copy the requirements file into the container
  COPY requirements.txt .

  # Install the necessary dependencies
  RUN pip install --no-cache-dir -r requirements.txt

  # Update OS libraries and install VI editor
  RUN apt-get update && apt-get install -y vim

  # Default command that is triggered when container starts
  CMD ["tail", "-f", "/dev/null"]
  ```

  * `FROM` is used to specify the base image for the Dockerfile. In this case, the official Python 3.10 image is used as the base.
  * `WORKDIR` is used to set the working directory for the rest of the instructions in the Dockerfile. In this case, the working directory is set to /app.
  * `COPY` is used to copy files and directories from the host machine to the container. In this case, the requirements.txt file is copied to the /app directory.
  * `RUN` is used to execute commands in the container. In this case, pip install is run to install the dependencies listed in requirements.txt
  * `CMD` is used to specify the command that should be run when the container starts. In this case, the tail command is used to display the last lines of a file and the -f option is used to keep the command running and display new lines as they are added to the file. By using tail -f /dev/null you are not looking at any file but it keeps running

### Step 3 - Requirements file

* Create a file named `requirements.txt` with following content:

  ```txt
  psycopg2==2.9.5
  ```

  > psycopg2 is a PostgreSQL library for Python. It is used to connect to, query and manage a PostgreSQL database from a Python script.

### Step 4 - Start the composer

* Run the containers

  ```sh
  docker-compose up -d
  ```

  >This command will pull the required images, create the containers, and start them in detached mode.

### Step 5 - Verify containers state

* Check the running containers

  ```sh
  docker-compose ps
  ```
