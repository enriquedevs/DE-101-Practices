# Python Overview and Running Applications on Containers

In this practice we will develop and use a Python application running on a docker container

![Docker-Python](documentation_images/docker-python.png)

### Prerequisites
* [Install docker](https://docs.docker.com/engine/install/) 

### What You Will Learn
- How to use a docker container of a Python Application
- Docker Compose commands
- Operative System commands and Overview
- How to connect to a Docker Container
- How to connect to a Database by using a DB client
- Programming foundations
- Python Overview

# Practice

You are working on a Zoo, and the Zoo is asking you to create a software that classifies the animals of the Zoo.

This Zoo only passed you a list of the classification of the animals, and you will write a software that classifies them.

Once classification is done, store them into a database.

![img](documentation_images/zoo.png)


### Requirements
* Develop and setup a docker compose to use python on a container
* Develop classes for the following animal classification:
  * **Mammals:** lions, elephants, monkeys, bears, giraffes
  * **Birds:** parrots, eagles, flamingos, penguins, owls
  * **Reptiles:** snakes, lizards, crocodiles, turtles, iguanas
  * **Fish:** sharks, rays, piranhas, clownfish, salmon
  * **Amphibians:** frogs, toads, newts, salamanders, axolotls
* Use Python's data to deposit on a PostgreSQL Database

# Let's do it!


## Step 1

First, we are going to create a docker-compose.yml file with the configuration for a python and postgreSQL container

```
version: '3'
services:
  postgres_db:
    image: postgres:11.1
    environment:   # Set up postgres database name and password
      POSTGRES_PASSWORD: password
      POSTGRES_DB: bookstore
      POSTGRES_USER: root
    ports:    # Set up ports exposed for other containers to connect to
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

networks:
  app-tier:
    driver: bridge
```

### Docker compose
**Docker Compose is a tool for defining and running multi-container Docker applications. It allows you to configure your application's services, networks, and volumes in a single docker-compose.yml file, and then start and stop them using a single command.**

Now let's run the containers with following docker compose command:

```
docker-compose up -d
```

This command will pull the required images, create the containers, and start them in detached mode.
