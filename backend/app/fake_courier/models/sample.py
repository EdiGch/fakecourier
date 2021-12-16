import uuid
from typing import List, Dict, Tuple

from sqlalchemy import Column, String, update
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.fake_courier.exceptions import NotFoundException


class SampleModel(Base):
    __tablename__ = "sample"

    FIELDS_NAMES_MAP = {}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    @classmethod
    async def get_by_id(cls, db, entity_id: uuid.UUID, options=None) -> "SampleModel":
        """
        Return `SampleModel` with given ID.

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        options = options if options else []
        query = cls.get_configured_query(options)
        results = await db.execute(query.filter_by(id=entity_id))
        sample = results.scalars().first()

        if not sample:
            raise NotFoundException(message=f"id={entity_id}")

        return sample

    @classmethod
    async def get_all(
        cls,
        db,
        options=None,
    ) -> Tuple[Dict, List["SampleModel"]]:
        """
        Return `SampleModel` list

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        query = SampleModel.get_configured_query(options)

        return (await db.execute(query)).scalars().all()

    @classmethod
    async def add(
        cls,
        db,
        entity: Dict,
        commit: bool = True,
    ) -> "SampleModel":
        """
        Adds new row to SampleModel table.
        Args:
            entity: object, that will be added.
            commit: commit
        """
        updatable_fields = cls.get_updatable_fields_from_dict(entity)
        instance = cls(**updatable_fields)
        db.add(instance)
        await db.flush()
        if commit:
            await db.commit()
            await db.refresh(instance)

        return instance

    @classmethod
    async def update(cls, db, sample_id: str, entity: Dict, commit: bool = True) -> "SampleModel":
        """
        Updates row to SampleModel table.
        Args:
            entity: row id, that will be updated.
            sample_id:
            commit: commit
        """
        brief = await db.get(cls, sample_id, [])

        updatable_fields = cls.get_updatable_fields_from_dict(entity)

        update_command = update(cls).where(cls.id == sample_id).values(updatable_fields)
        await db.execute(update_command)
        if commit:
            await db.commit()
            await db.refresh(brief)
        return brief

    @classmethod
    async def delete(cls, db, entity_id: str, commit: bool = True) -> None:
        """
        Deletes row from SampleModel table.
        Args:
            entity_id: row id, that will be deleted.
            commit: commit
        """
        brief = await db.get(cls, entity_id)

        if brief is None:
            raise NotFoundException(debug_msg=f"id={entity_id}")

        await db.delete(brief)
        await db.flush()

        if commit:
            await db.commit()
