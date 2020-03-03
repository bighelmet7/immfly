FROM python:3

LABEL "autor"="Abner Andino"
LABEL "github"="@bighelmet7"
LABEL "version"="1.0"
LABEL "description"="Immfly interview test"

RUN apt-get update

WORKDIR /opt/immfly-dockerize
ADD /immfly /opt/immfly-dockerize

RUN mkdir -p static
RUN mkdir -p /var/logs/immfly && touch /var/logs/immfly/immfly.logs

RUN pip install -r requirements.txt
RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py collectstatic -link --noinput

RUN python manage.py createsuperuser --username immfly --email immfly@examen.com --noinput

EXPOSE 8080

CMD ["daphne", "-b" , "0.0.0.0", "-p", "8080", "immfly.asgi:application", "--access-log", "/var/logs/immfly/immfly.logs"]