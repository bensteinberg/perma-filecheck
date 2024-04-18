Microservice to check files for expected file type, extension, and antivirus.

[![Tests](https://github.com/harvard-lil/perma-filecheck/actions/workflows/tests.yml/badge.svg)](https://github.com/harvard-lil/perma-filecheck/actions)

## Local install

    docker compose up
    docker compose exec web bash

Commands starting with `#` are run inside `docker compose exec web bash`.

## Local development

Start the web server:

    # uvicorn main:app --reload --host 0.0.0.0

Check a file:

    curl -F 'file=@test_assets/test.gif' http://127.0.0.1:8000/scan/
    {"safe":true}

Add a dependency; it's essential to update `requirements.txt`, as that's what's used to build the Docker image:

    poetry add <packagename>
    poetry export -o requirements.txt
    docker compose up -d --build  # to reinstall requirements in the container

Run lints and tests:

    docker compose exec web flake8
    docker compose exec web pytest

Tests will fail if test coverage goes below 100%.

# Deployment

* Service has no auth, so limit to allowed IPs
* run server as `uvicorn main:app`
* server must be running `clamd` with regularly updated antivirus definitions
