FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1

# install clamav
# https://www.clamav.net/documents/installing-clamav#debian
RUN apt-get update \
    && apt-get install -y clamav clamav-daemon

RUN freshclam

# pip
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install pip==20.2.4  \
    && pip install -r requirements.txt --src /usr/local/src \
    && rm requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

COPY main.py /app/main.py
