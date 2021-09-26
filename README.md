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