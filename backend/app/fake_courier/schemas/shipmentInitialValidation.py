from typing import List, Optional, Dict, Union, Any
from pydantic import BaseModel
from app.fake_courier.schemas.shipmentAddress import ShipmentAddressModelSchema
from app.fake_courier.schemas.shipmentProduct import ShipmentProductModelSchema
import uuid


def get_shipment_address():
    shipment_address = ShipmentAddressModelSchema()
    return shipment_address


def get_shipment_product():
    product_list = []
    shipment_product = ShipmentProductModelSchema()
    product_list.append(shipment_product)
    return  product_list


class ShipmentInitialValidationModelSchema(BaseModel):
    class Config:
        orm_mode = False
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "UnitAmount": "3",
                "Ref1": uuid.uuid4().hex.upper()[0:12],
                "Ref2": "",
                "DeliveryRemark": None,
                "CODValue": 120.0000,
                "CommissionType": 2,
                "Cosignee": get_shipment_address(),
                "CODCurrency": 0,
                "Commissions": get_shipment_product(),
            }
        }

    UnitAmount: Optional[str]
    Ref1: Optional[str]
    Ref2: Optional[str]
    DeliveryRemark: Optional[str]
    CODValue: Optional[str]
    CommissionType: Optional[str]
    Cosignee: Optional[Union[List, Dict]]
    CODCurrency: Optional[str]
    Commissions: Optional[Union[List, Dict]]
    validations: Optional[Any]
    status: Optional[str]
    error: Optional[str]
