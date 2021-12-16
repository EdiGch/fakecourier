import logging
import os
from typing import Generator

from alembic.command import upgrade as alembic_upgrade, downgrade as alembic_downgrade
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient

from app.app import create_app
from app.conf import settings
from .fixtures import *  # noqa

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def db():
    alembic_config = AlembicConfig("alembic.ini")
    os.environ["DB_URI"] = settings.SQLALCHEMY_DATABASE_URI
    alembic_downgrade(alembic_config, "base")
    alembic_upgrade(alembic_config, "head")


@pytest.fixture(scope="function")
def client() -> Generator:
    app = create_app()
    # app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
