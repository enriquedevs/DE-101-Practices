# Pre-Setup

## Pre-requisites

- Install Docker
- Install Docker Compose

## Build and start the environment

Start up the docker containers by running the following command in the current directory.

```sh
./start.sh
```

>If you cannot run the shell script, you can run the commands in the script manually, one by one. Notice that the first time you run this command it will take up to 30 minutes to download and build the images.

Now, run the following command to check that the containers are running. Make sure that all the containers are in the `healthy` state.

```sh
docker ps
```

>If that is not the case, run the `stop.sh` script and and then the `start.sh` script again.
