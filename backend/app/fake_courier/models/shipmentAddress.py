import uuid
from typing import List, Dict, Tuple
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.db.base import Base
from app.fake_courier.exceptions import NotFoundException
from datetime import datetime


class AddressModel(Base):
    __tablename__ = "shipment_address"

    FIELDS_NAMES_MAP = {}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    shipment_id = Column(Integer, ForeignKey('shipment.id'))
    country_code = Column(String(255), nullable=False)
    zipcode = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    street_and_number = Column(String(255), nullable=False)
    telephone = Column(String(255), nullable=False)
    fax = Column(String(255), nullable=True)
    notify_gsm = Column(String(255), nullable=False)
    notify_email = Column(String(255), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow())

    @classmethod
    async def get_all(
        cls,
        db,
        options=None,
    ) -> Tuple[Dict, List["AddressModel"]]:
        """
        Return `AddressModel` list

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        query = AddressModel.get_configured_query(options)

        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, db, entity_id: int, options=None) -> "AddressModel":
        """
        Return `AddressModel` with given ID.

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
    async def add(
        cls,
        db,
        entity: Dict,
        commit: bool = True,
    ) -> "AddressModel":
        """
        Adds new row to AddressModel table.
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
