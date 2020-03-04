# Immfly exam

[![Build Status](https://travis-ci.com/bighelmet7/immfly.svg?token=qVuyqSjnTjTxdCoTkHDd&branch=master)](https://travis-ci.com/bighelmet7/immfly)

[![codecov](https://codecov.io/gh/bighelmet7/immfly/branch/master/graph/badge.svg)](https://codecov.io/gh/bighelmet7/immfly)


Technical exam that emulates a small entertainment service.

# Requirements

 - virtualenv
 - python3.8
 - docker
 - git

## Installation & Local run

 - Without docker:
 
    ```bash
    virtualenv --python=python3 immfly/.env && source immfly/.env/bin/activate
    ```
    ```bash
    git clone https://github.com/bighelmet7/immfly.git immfly/src
    ```
    ```bash
    cd immfly/src/immfly && pip install -r requirements
    ```
    ```bash
    python manage.py test
    ```
    ```bash
    daphne -b 0.0.0.0 -p 8080 --access-log /var/logs/immfly/immfly.logs immfly.asgi:application
    ```
 - With docker:
    ```bash
    docker-compose up
    ```

## TODO

- dummy sql file instead of adding manually the values.
- CI with gitlab
- docker secrets for the plain text posswords
- kubernetes implementation
- nginx as a reverse proxy.

## Stack

Python is the main core of all service with Django as a webservice.

django-restframework, is the mostly important Python frameworks to mention.
Docker and docker-compose

## Model
The propouse structure is:

TreeChannel will be where all the main roots will live. For example Root
ChannelNode contains a reference to TreeChannel so we can identify our main tree, also contains a recursive reference
to it self so can have subchannels.
Content contents that a subchannel can have.

So we have: TreeChannel <--> ChannelNode <---> ChannelNode (subchannels) <---> Contents

## Endpoints

| ROUTE |  METHOD | DATA
|--|--|--|
| /api/v1/channel| GET | - |
| /api/v1/tree | GET | - |
| /api/v1/content | GET | - |
| /api/v1/language | GET | - |

## Volumes:
If you are working with docker there are some volumes set for persistence data, as:
/data/postgres volume for our postgres DB.
/data/immfly volume for saving the logs of /var/logs/immfly/immfly.logs
/data/files volume for retrieve the rating_values.cvs file given by the django command.

# Django
The default user for this exam is test with password immfly1234. The Django-admin site contains the models necessary
to add Channels, SubChannels, Tree and Langugages.

The demanded command for calculating all the rate values is:

```bash
python manage.py rating_value <NAME_OF_A_ROOT_IN_A_TREE>
 ```
