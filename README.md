# timestamped_kvstore
A Key-value-timestamp store wrapped by a rest api in Python.

This is an attempt to locally setup a trino sql engine with a iceberg rest api catalog, that is then polled using a python rest api.
We were successful in spinning up all the services, and to make all components communicate with each other, but 
we were unsuccessful in forcing the iceberg rest api service to use our mounted volume as the metastore.

Currently the fastapi application is pointing to the non optimal postgres database solution, which satisfies our requirement for an key-value store, and is optimal when purely considering latency on transactional workloads, but will not scale well for analytics purposes. 

The former will be a much better choice for analytics purposes.


# How to run
We need a couple of dirs as our persistent volumes. I have not included them here to avoid permissions problems.

### Requirements
1. create directories data/iceberg_warehouse and data_pg, with the following commands:
  - `mkdir -m 777 data_pg` 
  - `mkdir -m 777 data && mkdir -m 777 data/iceberg_warehouse`
2. Docker or podman
3. docker-compose or podman-compose
4. inspect the docker-compose.yml and ensure that there are no applications actively listening on the mentioned ports. 

### RUN
to run the fastapi and the databases, just run the following podman-compose command. 
- `podman-compose up --build -d`

upon deployment you should be able to call the rest api using the curl command like 
- `curl -X PUT http://localhost:8080 -H 'Content-Type: application/json' -d '{"key": "mykey", "value": "myvalue", "timestamp" : 1673524092123456}'`
- `curl -X GET http://localhost:8080 -H 'Content-Type: application/json' -d '{"key":"mykey", "timestamp": 1673524092123456}'`