Fake Courier Backend
====================

# Install
To install app run:

`pip install -r requirements.*`
then install developer packages

# Run
To run invoke:
`python dev-main.py` or `uvicorn main:app --reload --host 0.0.0.0`


# Tests
To run tests invoke below command:
`pytest --docker-compose=tests/docker-compose-tests.yaml`


# Migrations
generate:
`alembic revision --autogenerate -m "Sample table"`
make migration:
`alembic upgrade head`
