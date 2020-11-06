# Hållbar Skolmåltid server

This is the repository for the backend for the Hållbar Skolmåltid backend, started June 2020. The backend provides aggregated school data, for the project's frontend apps as well as direct api access.

The current setup encompasses
* A mongo db
* FIWARE Orion Context broker - the context data is accessed using the standardized [NGSIv2 REST API](https://telefonicaid.github.io/fiware-orion/api/v2/stable/).
*  ~~*FIWARE Comet - the historical context data component - [Comet docs](https://fiware-sth-comet.readthedocs.io/)*~~
* FIWARE Draco - basically an instance of [Apache NiFi](https://en.wikipedia.org/wiki/Apache_NiFi) - for automating the flow of data between systems. Potentially useful for shuffling (and transforming)  data from sources into the backend.
* FIWARE Keyrock - Identity Management [Keyrock docs](https://fiware-idm.readthedocs.io/) - adds OAuth2-based authentication and authorization security to orion access

<!-- language: lang-none -->

     +-------+
     | MySQL |
     |  DB   |
     +---+---+
         |
    +----+----+   +---------+
    | Keyrock +---+ Postman |
    |  IDM    |   |         |
    +----+----+   +----+----+
         |             |
     +---+---+   +-----+-----+  +-------+  +-------+
     | Front +---+   Wilma   +--+ Orion +--+ Mongo |
     |  End  |   | PEP Proxy |  |       |  |  DB   |
     +-------+   +-----------+  +-------+  +-------+


## Prerequisites

It is assumed that Docker is installed on the host.
If that is not the case, follow [Docker's installation instructions](https://docs.docker.com/install/).

## Installation

<done first time during start, see below>

## Execution

### Starting
To start the backend, do the following:

```bash
server/docker> docker-compose up
```

The first startup takes a while, since all containers are downloaded/built.

### Persistent orion data
*(Keyrock data currently in a mysql volume)*

**For empty database** - first time, or if mongo volume has been removed ... to initiate with some test data, either

**import** *hallbar_skolmaltid_server_init* collection in [Postman](https://www.postman.com/) and run (locally, or change collection variables accordingly) collection using Postman 'Runner' feature.

**OR**

<details style="background-color=grey">
  <summary> <b>restore</b> a saved database dump</summary>
  
  #### Restore
  Copy to container:

      server/docker> docker cp ../200618_rise_mongo.tar.gz db-mongo:/dump.tar.gz

  Uncompress:

      server/docker> docker exec db-mongo tar -xvzf dump.tar.gz

  Restore:

      server/docker> docker exec -it db-mongo mongorestore /dump

  #### Save
  Dump:

      server/docker> docker exec -it db-mongo mongodump --host localhost --port 27017 -o dump

  Compress:

      server/docker> docker exec -it db-mongo tar -zcvf 200618_rise_mongo.tar.gz dump

  Copy to host

      server/docker> docker cp db-mongo:/200618_rise_mongo.tar.gz ../

---
</details>

### Stopping
Stopping while keeping all data (orion/comet/keyrock data in volumes)

    server/docker> docker-compose down

... or if you don't need to keep _any_ of your local volumes, the simplest is to remove them all when stopping

    server/docker> docker-compose down -y

... or if you have other volumes you want to keep, just use _docker volume rm_ to delete one by one after stopping.

## Usage

### Mongo DB
Used by both Orion and Comet.
Currently mapped to a local volume, which will be restored on start, unless you explicitly delete it.

### Orion/Comet
Some simple examples of using the orion/comet api are available as a postman collection in this directory.
[Orion API here](https://telefonicaid.github.io/fiware-orion/api/v2/stable/), [Comet docs here](https://fiware-sth-comet.readthedocs.io/en/latest/)

Some examples:

Query orion for all schools, just getting ids

  http://{{orion}}/v2/entities?type=School&attrs=id

Query orion for entire user1

  http://{{orion}}/v2/entities/user1
  
Query orion for user1's related school1's schoolAttendanceObserved between dates:

  http://{{orion}}/v2/entities?type=SchoolAttendanceObserved&q=refSchool==school1;dateObserved==2020-02-01T10:00:00.00Z..2020-02-03T10:00:00.00Z

~~E.g. query comet for last three updates of schoolAttendance1~~

  ~~http://{{sth-comet}}/STH/v1/contextEntities/type/SchoolAttendance/id/schoolAttendance1/attributes/attendance?lastN=3~~

### Draco
The web GUI is available at http://localhost:9090/nifi

Currently the "flow" is saved/mapped from the server/docker/draco/conf directory.

Draco normally updates flow files in *server/docker/draco/conf* while running. If you're not working with the draco configuration, try not to commit these new/changed files.

### Current demo scenario
* As before, build/start according _Starting_ above
* As before, load data using _hallbar_skolmaltid_server_init_ postman collection, see above (collection may have been updated!)
* Use the _orion_via_pepproxy_ postman collection for usage ideas
  - user1 login to keyrock: _USER1/Keyrock - create keyrock token_
  - get user1's id: _USER1/Keyrock - get own user id_
  - user1 get access token: _USER1/Keyrock - create access token_
  - get user1's related data using user1's id ...

Regarding users/authentication, it's using the same setup as [this tutorial](https://github.com/FIWARE/tutorials.PEP-Proxy#securing-the-orion-context-broker), look there for more info.
