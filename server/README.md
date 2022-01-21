# Hållbar Skolmåltid server

This is the repository for the backend for the Hållbar Skolmåltid backend, started June 2020. The backend provides aggregated school data, for the project's frontend apps as well as direct api access.

## Future considerations
- Because of shifting goals from the initial statistics data focus, using fiware components and data models could be made more efficient with a regular application server.
- Because of shifting goals regarding vklass involvement, making the attendance data handling switchable between fetching live and generating dummy data has been unecessaary complicated. Hence, the later additions of meal and waste data was made very simple.
- Because of the solution becoming more of a concept, and only (barely) having one source of every type of data, using Draco/NiFi is not motivated

## Attendance data
The initial idea was to only provide open data for school attendance statistics, with daily data retreived from various school data services (currently only vklass). Thus, fiware seemed a good choice for its open standardised api/datamodels used in other public sector open data activities (see DIGG's guidelines), in combination with draco/nifi for funneling and transcoding data. Also, this was seen as a good fiware learning occassion.  
However, with conditions changing during the project, vklass data access got stuck in municipal agreements, hence a dummy server was created to emulate a vklass server answering the calls we need with some data, and with time the requirements for that data grew. Skipping the vklass compatibility requirement would make that code easier.  
Also, after a while, with the added requirement of handling sensitive data, authentication/authorization was needed, which was more complicated for the fiware generic enablers as opposed to just using a regular application server.

## Meal data
Concerns daily school food data, currently only from partner Mashie. Since the prototype has turned into a concept prototype, and there was (temporary?) very limited fake data from Mashie, no continous fetching of data was deemed necessary - one month's worth of data for one distributor was downloaded and rotated.

## System setup
The current setup encompasses
* A mongo db
* FIWARE Orion Context broker - the context data is accessed using the standardized [NGSIv2 REST API](https://telefonicaid.github.io/fiware-orion/api/v2/stable/).
*  ~~*FIWARE Comet - the historical context data component - [Comet docs](https://fiware-sth-comet.readthedocs.io/)*~~
* FIWARE Draco - basically an instance of [Apache NiFi](https://en.wikipedia.org/wiki/Apache_NiFi) - for automating the flow of data between systems. Potentially useful for shuffling (and transforming)  data from multiple sources into the backend.
* FIWARE Keyrock - Identity Management [Keyrock docs](https://fiware-idm.readthedocs.io/) - adds OAuth2-based authentication and authorization security to orion access

<!-- language: lang-none -->

     +-------+
     | MySQL |
     |  DB   |
     +---+---+
         |
    +----+----+                              +-------+
    | Keyrock |                              | Mongo |
    |  IDM    |                              |  DB   |
    +----+----+                              +-------+
         |                                  /
     +---+---+   +-----+-----+   +--------+
     | Front +---+   Wilma   +---+ Orion  |
     |  End  |   | PEP Proxy |   |        |
     +-------+   +-----------+   +---+----+             vklass server
                               /     |      \          /
                    +--------+   +---+----+   +-------+
                    | mashie |   | waste  |   | Draco |
                    | dummy  |   | dummy  |   |  NiFi |
                    +--------+   +--------+   +-------+
                                                        \
                                                          +--------+
                                                          | vklass |
                                                          | dummy  |
                                                          +--------+


## Prerequisites

It is assumed that Docker is installed on the host.
If that is not the case, follow [Docker's installation instructions](https://docs.docker.com/install/).

## Installation

<done first time during start, see below>

## Execution

### Starting
To start the backend for **local development** (with vklass emuator):

```bash
server/docker> docker-compose up
```

To start the backend **on production server** (with vklass emuator):

```bash
server/docker> docker-compose -f docker-compose.yml -f docker-compose.server.yml up -d
```

The first startup takes a while, since all containers are downloaded/built.
<details style="background-color=grey">
  <summary> <b>Current issues</b> </summary>
  
  - Potential starting timing issues with proxies, they may need a manual start.
  - The last call from postman init collection not working remotely, use curl locally on server instead.
  - If all else fails - stop, delete all data directories, delete images, checkout repo version of server/docker/draco folder ... and start again.
</details>

### Persistent orion data
*(Keyrock data currently in a mysql volume)*

**For empty database** - first time, or if mongo volume has been removed ... to initiate with some test data, either

**import** *hallbar_skolmaltid_server_init* collection in [Postman](https://www.postman.com/) and run (locally, or change collection variables accordingly) collection using Postman Runner/Run feature (**NOTE for running on server**: 210604 we had issues with the 'Trigger dailyinit' call to go through server firewalls, so we executed it locally on the server using 'curl -X POST localhost:9091/dailyinit' when fiware-draco had started up).

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
To stop while keeping all data (orion/comet/keyrock data in volumes), for your docker-compose command exchange _up_ for _down_.
If you don't need to keep _any_ of your local volumes, for your docker-compose command exchange _up_ for _down -v_.

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

### Keyrock IDM
The web GUI is so far available at http://localhost:3005/<br>
For now there is an admin user - alice-the-admin@test.com / test

See e.g. this [Securing Access](https://fiware-tutorials.readthedocs.io/en/latest/securing-access) tutorial for more info ...

### Current demo scenario
* As before, build/start according _Starting_ above
* As before, load data using _hallbar_skolmaltid_server_init_ postman collection, see above (collection may have been updated!)
* Use the _orion_via_pepproxy_ postman collection for usage ideas
  - user1 login to keyrock: _USER1/Keyrock - create keyrock token_
  - get user1's id: _USER1/Keyrock - get own user id_
  - user1 get access token: _USER1/Keyrock - create access token_
  - get user1's related data using user1's id ...

Regarding users/authentication, it's using the same setup as [this tutorial](https://github.com/FIWARE/tutorials.PEP-Proxy#securing-the-orion-context-broker), look there for more info.
