import logging
from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from random import randint
import datetime
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.deps import get_db
from app.fake_courier.schemas import ShipmentModelSchema, ShipmentChangeStatusModelSchema
from app.fake_courier.schemas import ShipmentInitialValidationModelSchema
from app.fake_courier.models import ShipmentModel
from app.fake_courier.factories.shipment import ShipmentFactory
from app.fake_courier.models.shipmentAddress import AddressModel
from app.fake_courier.factories.shipmentAddress import ShipmentAddressFactory
from app.fake_courier.models.shipmentProduct import ShipmentProductModel
from app.fake_courier.factories.shipmentProduct import ShipmentProductFactory
from app.fake_courier.factories.responseModel import ResponseModel
from app.fake_courier.models.shipmentStatus import ShipmentStatusModel
from app.fake_courier.schemas.shipmentStatus import ShipmentStatusModelSchema
from app.fake_courier.statuses.courierStatuses import CourierStatuses

router = APIRouter(dependencies=[])
logger = logging.getLogger(__name__)

shipments_v1_templates = Jinja2Templates(directory="app/templates/shipments")


@router.get(
    "",
    status_code=HTTPStatus.OK
)
async def shipments_get(
        *,
        db=Depends(get_db),
):
    shipments = await ShipmentModel.get_all(db=db)
    return shipments


@router.get(
    "/{shipment_id}",
    status_code=HTTPStatus.OK,
    response_model=ShipmentModelSchema,
)
async def shipment_get(
        *,
        db=Depends(get_db),
        shipment_id: int,
):
    shipment = await ShipmentModel.get_by_id(db=db, entity_id=shipment_id)
    return shipment


@router.post(
    "/shipmentsbyid",
    status_code=HTTPStatus.OK
)
async def shipments_by_id(
        *,
        db=Depends(get_db),
        shipments_id: List[str]
):
    shipment = await ShipmentModel.get_shipments_by_tracking_no(db=db, entity_ids=shipments_id)

    if shipment is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"Shipment Doesn't Exist"},
        )

    return shipment


@router.post(
    "/shipment/change-status",
    status_code=HTTPStatus.OK,
)
async def shipment_change_status(
        *,
        db=Depends(get_db),
        request: Request,
        _: ShipmentChangeStatusModelSchema,
):
    payload = await request.json()
    tracking_no_from_cabroz = payload.get('tracking_no_from_cabroz')
    status_id = payload.get('status_id')

    shipment = await ShipmentModel.get_shipment_by_tracking_no(db=db, entity_id=tracking_no_from_cabroz)
    if shipment is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"Not found shipment"},
        )

    courier_statuses = CourierStatuses()
    status = courier_statuses.get_by_value_from_dict(status_id)

    if status is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"Not found status"},
        )

    shipment_status_model_schema = ShipmentStatusModelSchema()
    shipment_status_model_schema.shipment_id = shipment.id
    shipment_status_model_schema.status_code = status['StatusID']

    await ShipmentStatusModel.add(
        db=db,
        entity=shipment_status_model_schema.__dict__,
    )

    return {"message": "A new status has been added"}


@router.post(
    "/createshipment",
    status_code=HTTPStatus.OK
)
async def shipment_post(
        *,
        db=Depends(get_db),
        request: Request,
        _: ShipmentInitialValidationModelSchema
):
    payload = await request.json()

    try:
        ShipmentModelSchema.parse_obj(payload)
    except ValidationError as e:
        list_validation = []
        for obj in e.errors():
            validation_dict = {
                "Code": randint(1000, 1500),
                "Message": obj['loc'][0] + ' ' + obj['msg']
            }
            list_validation.append(validation_dict)

        error_dict = {
            "Code": randint(1000, 1500),
            "Validations": None,
            "Severity": 4,
            "Context": None,
            "StackTrace": "at MortyCore.Controller.CreateShipmentController",
            "Message": "Validacija nije uspjela, provjerite potvrde za detalje!",
            "Data": {},
            "InnerException": None,
            "HelpLink": None,
            "Source": "MortyExtensions",
            "HResult": -2146232832
        }

        response_model = ResponseModel(None, None, None, None, None, None, 1, error_dict, list_validation)
        return response_model

    shipment_factory = ShipmentFactory(
        payload.get('UnitAmount'),
        payload.get('Ref1'),
        payload.get('Ref2'),
        payload.get('DeliveryRemark'),
        str(payload.get('CODValue')),
        payload.get('CommissionType'),
        payload.get('CODCurrency')
    )

    shipment = await ShipmentModel.add(
        db=db,
        entity=shipment_factory.__dict__,
    )

    address_factory = ShipmentAddressFactory(
        payload.get('Cosignee')['Name'],
        shipment.id,
        payload.get('Cosignee')['CountryCode'],
        payload.get('Cosignee')['Zipcode'],
        payload.get('Cosignee')['City'],
        payload.get('Cosignee')['StreetAndNumber'],
        payload.get('Cosignee')['Telephone'],
        payload.get('Cosignee')['Fax'],
        payload.get('Cosignee')['NotifyGSM'],
        payload.get('Cosignee')['NotifyEmail']
    )

    await AddressModel.add(
        db=db,
        entity=address_factory.__dict__,
    )

    for obj in payload.get('Commissions'):
        shipment_product_factory = ShipmentProductFactory(obj.get('ItemCode'), obj.get('Amount'), shipment.id)
        await ShipmentProductModel.add(
            db=db,
            entity=shipment_product_factory.__dict__,
        )

    courier_statuses = CourierStatuses()

    shipment_status_model_schema = ShipmentStatusModelSchema()
    shipment_status_model_schema.shipment_id = shipment.id
    shipment_status_model_schema.status_code = courier_statuses.ddef

    await ShipmentStatusModel.add(
        db=db,
        entity=shipment_status_model_schema.__dict__,
    )

    delivery_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return ResponseModel(shipment.tracking_no, None, None, delivery_time, delivery_time, None, 0, None, [])
