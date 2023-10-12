# Pre-Setup

## Pre-requisites

- Install Docker
- Install Docker Compose

### Docker Compose

First create a `docker-compose.yml` file with the following contents. We will add one service at a time.

```yml
version: "3"

services:
```

#### MinIO

First, add the MinIO service to the `docker-compose.yml` file. MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service.

```yml
  minio:
    image: minio/minio
    container_name: minio
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
    ports:
      - 9001:9001
      - 9000:9000
    command: ["server", "/data", "--console-address", ":9001"]
```

#### MinIO Client

Next, add the MinIO Client service to the `docker-compose.yml` file. The MinIO Client is a command line tool for interacting with the MinIO server. This `entrypoint` command will create a bucket called `minio` and add a directory called `warehouse` to the bucket.

```yml
  mc:
    depends_on:
      - minio
    image: minio/mc
    container_name: mc
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
    entrypoint: >
      /bin/sh -c "
      until (/usr/bin/mc config host add minio http://minio:9000 admin password) do echo '...waiting...' && sleep 1; done;
      /usr/bin/mc rm -r --force minio/warehouse;
      /usr/bin/mc mb minio/warehouse;
      /usr/bin/mc policy set public minio/warehouse;
      exit 0;
      "
```

#### Iceberg

Now, add the Iceberg REST catalog service to the `docker-compose.yml` file. This service simply exposes a REST interface for Spark to connect to. Spark doesn’t need to be concerned with connecting to the actual datastore which can be anything ranging from a Hive metastore to a MySQL database.

```yml
  rest:
    image: tabulario/iceberg-rest:0.2.0
    ports:
      - 8181:8181
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
      - CATALOG_WAREHOUSE=s3a://warehouse/wh/
      - CATALOG_IO__IMPL=org.apache.iceberg.aws.s3.S3FileIO
      - CATALOG_S3_ENDPOINT=http://minio:9000
```

#### Spark + Iceberg

Finally, add the `spark-iceberg` service to the `docker-compose.yml` file. This service is described in the `Dockerfile` inside the `spark` directory in this repository. Please refer to the specification if you want to know more about the image.

```yml
  spark-iceberg:
    build:
      context: ./spark
      dockerfile: Dockerfile
    container_name: spark-iceberg
    depends_on:
      - rest
      - minio
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
    ports:
      - 8888:8888
      - 8080:8080
      - 10000:10000
      - 10001:10001
    links:
      - rest:rest
      - minio:minio
```

### Build and start the environment

Start up the Icebeberg and PySpark environment by running the following.

```sh
docker-compose up --build
```

You can then access the MinIO UI at <http://localhost:9000>. The Username is `admin` and the password is `password`.

MinIO is a local replacement for S3. It is a simple object storage server that is compatible with the Amazon S3 API. It is used in this practice to simulate a cloud storage environment.

You also can access the PySpark REPL by running the following.

```sh
docker exec -it spark-iceberg pyspark
```

Run the following command to confirm that the `spark` session successfully started. We will use this session to interact with Iceberg.

```py
spark.sparkContext.getConf().getAll()
```
