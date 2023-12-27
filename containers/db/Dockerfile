FROM postgres:12

ADD create.sql /docker-entrypoint-initdb.d
ADD testdb.dump /docker-entrypoint-initdb.d

RUN apt-get update && apt-get install -y \
postgis postgresql-12-postgis-3