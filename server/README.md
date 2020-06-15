# Hållbar Skolmåltid server

This is the repository for the backend for the Hållbar Skolmåltid backend, started June 2020. The backend provides aggregated school data, for the project's frontend apps as well as direct api access.

The current setup encompasses
* A mongo db
* FIWARE Orion Context broker - the context data is accessed using the standardized [NGSIv2 REST API](https://telefonicaid.github.io/fiware-orion/api/v2/stable/).
* FIWARE Comet - the historical context data component - [Comet docs](https://fiware-sth-comet.readthedocs.io/en/latest/)
* FIWARE Draco - basically an instance of [Apache NiFi](https://en.wikipedia.org/wiki/Apache_NiFi) - for automating the flow of data between systems. Potentially useful for shuffling (and transforming)  data from sources into the backend.

## Prerequisites

It is assumed that Docker is installed on the host.
If that is not the case, follow [Docker's installation instructions](https://docs.docker.com/install/).

## Installation

...

## Execution

To start the backend, do the following:

    server/docker> docker-compose up

The first startup takes a while, since all containers are downloaded/built. To stop:

    server/docker> docker-compose down

## Usage

### Mango DB
Used by both Orion and Comet.
Currently mapped to a local volume, which will be restored on start, unless you explicitly delete it.

### Orion/Comet
Some simple examples of using the orion/comet api are available as a postman collection in this directory.

### Draco
The web GUI is available at http://localhost:9090/nifi
Currently the "flow" is saved/mapped from the server/docker/draco/conf directory.