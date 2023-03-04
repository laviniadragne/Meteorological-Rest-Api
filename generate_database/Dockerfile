FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD: my_secret_password \
            MYSQL_DATABASE: app_db

ADD creare_baza_de_date.sql /docker-entrypoint-initdb.d

EXPOSE 3306
