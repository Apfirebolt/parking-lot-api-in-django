# parking-lot-api-in-django
A parking lot API design and implementation in Python using Django Framework

# Made Using 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

# Overview

Designing a parking lot system is one of the most frequently asked questions in the system design for any major product based companies. In this repo, I implement my own version
of a parking design system in Django as an API using the Django rest framework package.

# Database Architecture

To be added later

# Class Diagram

To be added later

## How Docker volumes work?

Used the docker compose command to spawn off both the containers, delete db container and then created it again. The Database was still there. I used the following commands. The first command re-creates the db container, the second command creates both the containers for the first time.


```yaml
docker-compose up -d db

docker-compose up --build   
```

