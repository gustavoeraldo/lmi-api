# Set up 

Install pipenv

```bash
pip install pipenv

```

Activate the enviroment:

```bash
pipenv shell
```

Install project dependencies:

```bash
pipenv install
```

You can also install development dependencies:

```bash
pipenv install -d
```

You can install new packages using:

```bash
pipenv install package_name
```

And remeber to update the requirements.txt:

```bash
pipenv lock -r > requirements.txt
```

## How to run

```bash
uvicorn main:app --reload
```

## Deployment

```bash
docker-compose up --build -d
```
## Image update

```bash
# creating a Tag
docker tag lmi-api:v1 docker.pkg.github.com/gustavoeraldo/lmi-api/lmi-api:v1

# Push the image
docker push docker.pkg.github.com/gustavoeraldo/lmi-api/lmi-api:v1
```

## Alembic

If you are using pipenv:

```bash
pipenv shell

pipenv install alembic

alembic init migrations
```

Before create the tables, update alembic [configuration](/migrations/env.py) and then run: 
```
alembic revision --autogenerate -m "Added account table"

# or
alembic revision --autogenerate

alembic upgrade head
```

## To Do list
> things that I want to try.

- [ ] Use unity tests
- [ ] Use NGINX
- [ ] Use CI/CD with Git actions
- [ ] Use Celery so send emails
    - [ ] Use mongo or postgres to save logs. Figure out how to use a custom template with Celery to save data.
- [ ] Develop dynamic filters
- [ ] Create a docker yaml file
- [ ] Watch system logs
    - [ ] How organize logs
    - [ ] System monitoring
- [ ] Describe software architecture patterns used in this project.
- [ ] Use elastic search engine.
- [ ] Use Authentication
    - [ ] Use refresh tokens
    - [ ] Authentication with cookies
    - [X] Authentication with JWT using OAuth2
-[X] Auto generate migrations using alembic.


## Testing

```bash
pytest

# or
pytest --cov=app tests/

# generating html report from coverage
coverage html
```