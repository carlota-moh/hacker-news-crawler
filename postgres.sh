#!/bin/bash

docker pull postgres

docker run -itd -p 5432:5432 \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=1234 \
-v ~/db:/var/lib/postgresql/data \
--name hacker-db \
postgres
