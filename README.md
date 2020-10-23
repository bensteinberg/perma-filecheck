Microservice to check files for expected file type, extension, and antivirus.

## Local install

    $ docker-compose up
    $ docker-compose exec web bash

Commands starting with `#` are run inside `docker-compose exec web bash`.

## Local development

Start the web server:

    # uvicorn main:app --reload --host 0.0.0.0
    
Check a file:

    $ curl -F 'file=@test_assets/test.gif' http://127.0.0.1:8000/scan/
    {"safe":true}
    
Add a dependency:

* edit requirements.in
* run `pip-compile --allow-unsafe --generate-hashes`

Run tests:

    pytest

Tests will fail if test coverage goes below 100%.

# Deployment

* Service has no auth, so limit to allowed IPs
* run server as `uvicorn main:app`
* server must be running `clamd` with regularly updated antivirus definitions
