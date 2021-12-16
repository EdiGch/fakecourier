from typing import List, Dict, Tuple
from sqlalchemy import Column, String, Integer, DateTime
from app.fake_courier.schemas.shipment import ShipmentModelSchema
from app.fake_courier.schemas.shipmentAddress import ShipmentAddressModelSchema
from app.fake_courier.schemas.shipmentProduct import ShipmentProductModelSchema
from app.fake_courier.schemas.shipmentsByIdResponse import ShipmentsByIdDataResponse, ShipmentsByIdResponse, \
    ShipmentsEvents
from app.fake_courier.statuses.courierStatuses import CourierStatuses
from app.db.base import Base
from app.fake_courier.exceptions import NotFoundException
from datetime import datetime
import uuid


class ShipmentModel(Base):
    __tablename__ = "shipment"

    FIELDS_NAMES_MAP = {}

    id = Column(Integer, primary_key=True, index=True)
    tracking_no = Column(String(12), nullable=False, default=uuid.uuid4().hex.upper()[0:12])
    unit_amount = Column(String(10), nullable=False)
    ref1 = Column(String(25), unique=True, nullable=False)
    ref2 = Column(String(255), nullable=True)
    delivery_remark = Column(String(255), nullable=True)
    cod_value = Column(String(255), nullable=True)
    commission_type = Column(Integer, nullable=False)
    cod_currency = Column(Integer, nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow())

    @classmethod
    async def get_all(
            cls,
            db,
            options=None,
    ) -> Tuple[Dict, List["ShipmentModel"]]:
        """
        Return `ShipmentModel` list

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        query = ShipmentModel.get_configured_query(options)

        allResults = (await db.execute(query)).scalars().all()

        return allResults

    @classmethod
    async def get_by_id(cls, db, entity_id: int, options=None):
        """
        Return `ShipmentModel` with given ID.

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        options = options if options else []
        query = cls.get_configured_query(options)
        results = await db.execute(query.filter_by(id=entity_id))
        shipment = results.scalars().first()
        if not shipment:
            raise NotFoundException(message=f"id={entity_id}")

        shipment_model_schema = ShipmentModelSchema()
        shipment_model_schema.UnitAmount = shipment.unit_amount
        shipment_model_schema.Ref1 = shipment.ref1
        shipment_model_schema.Ref2 = shipment.ref2
        shipment_model_schema.DeliveryRemark = shipment.delivery_remark
        shipment_model_schema.CODValue = shipment.cod_value
        shipment_model_schema.CommissionType = shipment.commission_type
        shipment_model_schema.CODCurrency = shipment.cod_currency
        shipment_model_schema.Cosignee = []
        shipment_model_schema.Commissions = []

        results = await db.execute("SELECT * FROM shipment_address Where shipment_id = :val", {'val': shipment.id})
        address = results.fetchone()

        if not address:
            raise NotFoundException(message=f"The address has not been assigned id={entity_id}")

        addressModelSchema = ShipmentAddressModelSchema()
        addressModelSchema.Name = address.name
        addressModelSchema.CountryCode = address.country_code
        addressModelSchema.Zipcode = address.zipcode
        addressModelSchema.City = address.city
        addressModelSchema.StreetAndNumber = address.street_and_number
        addressModelSchema.Telephone = address.telephone
        addressModelSchema.Fax = address.fax
        addressModelSchema.NotifyGSM = address.notify_gsm
        addressModelSchema.NotifyEmail = address.notify_email

        shipment_model_schema.Cosignee = [addressModelSchema]

        results = await db.execute("SELECT * FROM shipment_product Where shipment_id = :val", {'val': shipment.id})
        products = results.fetchall()

        if not products:
            raise NotFoundException(message=f"The products has not been assigned id={entity_id}")

        products_list = []
        for obj in products:
            shipmentProductModelSchema = ShipmentProductModelSchema()
            shipmentProductModelSchema.ItemCode = obj.item_code
            shipmentProductModelSchema.Amount = obj.quantity
            products_list.append(shipmentProductModelSchema)

        shipment_model_schema.Commissions = products_list

        return shipment_model_schema

    @classmethod
    async def get_shipment_by_tracking_no(cls, db, entity_id: str, options=None):
        """
        Return `ShipmentModel` with given ID.

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        options = options if options else []
        query = cls.get_configured_query(options)
        results = await db.execute(query.filter_by(tracking_no=entity_id))
        shipment = results.scalars().first()
        if not shipment:
            raise NotFoundException(message=f"id={entity_id}")

        return shipment

    @classmethod
    async def get_shipments_by_tracking_no(cls, db, entity_ids: List[str], options=None):
        """
        Return `ShipmentModel` list

        `options` argument refers to SQLAlchemy Loader Options. See:
        https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#relationship-loading-with-loader-options
        """
        data_list = []
        for entity_id in entity_ids:
            events_list = []

            options = options if options else []
            query = cls.get_configured_query(options)
            results = await db.execute(query.filter_by(tracking_no=entity_id))
            shipment = results.scalars().first()

            details_of_shipment = ShipmentsByIdResponse()
            details_of_shipment.ShipmentID = shipment.tracking_no
            details_of_shipment.Ref1 = shipment.ref1
            details_of_shipment.Ref2 = shipment.ref2

            results = await db.execute("SELECT * FROM shipment_status Where shipment_id = :val", {'val': shipment.id})
            shipment_status = results.fetchall()
            courier_statuses = CourierStatuses()

            for status in shipment_status:
                status_dict = courier_statuses.get_by_value_from_dict(status.status_code)

                shipment_events = ShipmentsEvents()
                shipment_events.StatusID = status_dict['StatusID']
                shipment_events.StatusName = status_dict['StatusName']
                shipment_events.StatusDescription = status_dict['StatusDescription']
                events_list.append(shipment_events)

            details_of_shipment.Events = events_list

            data_list.append(details_of_shipment)

        data_for_the_answer_shipments_by_id = ShipmentsByIdDataResponse()
        data_for_the_answer_shipments_by_id.data = data_list
        data_for_the_answer_shipments_by_id.status = 0
        data_for_the_answer_shipments_by_id.validations = []

        return data_for_the_answer_shipments_by_id

    @classmethod
    async def add(
            cls,
            db,
            entity: Dict,
            commit: bool = True,
    ) -> "ShipmentModel":
        """
        Adds new row to ShipmentModel table.
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
