#!/bin/bash

docker exec -it $(docker ps | grep silesiasolar_backend | awk '{print $1}') python manage.py createsuperuser