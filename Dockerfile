FROM python:3

LABEL "autor"="Abner Andino"
LABEL "github"="@bighelmet7"
LABEL "version"="1.0"
LABEL "description"="Immfly interview test"

RUN apt-get update

WORKDIR /opt/immfly-dockerize
COPY /immfly /opt/immfly-dockerize

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8080