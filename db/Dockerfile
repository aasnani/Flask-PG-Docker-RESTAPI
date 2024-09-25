FROM postgres
COPY init.sql /docker-entrypoint-initdb.d
RUN chown postgres:postgres /docker-entrypoint-initdb.d/init.sql