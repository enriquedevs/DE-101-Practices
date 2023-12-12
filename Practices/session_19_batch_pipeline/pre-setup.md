# Pre-setup

## Prerequisites

* [Docker][install_docker]
* [Slack][slack]

## Steps

>The first time you run the commands can take up to 30 minutes to download and build the images.

### Step 1 - Images

Run the commands 1 by 1

```sh
docker build -t hadoop-base docker/hadoop/hadoop-base
docker build -t hive-base docker/hive/hive-base
docker build -t spark-base docker/spark/spark-base
```

### Step 2 - Composer

```sh
docker-compose up -d --build
```

### Step 3 - Slack

* Login to slack, use the credentials given by your instructor
* Add the `enroute-de101` workspace

![img](./img/slack-de101.png)

You can use the Web App/Mobile App/Desktop App

## Links

* [Install Docker][install_docker]

[install_docker]: https://docs.docker.com/engine/install/
[slack]: https://slack.com
