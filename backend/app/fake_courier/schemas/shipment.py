from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator, ValidationError
import uuid
from app.fake_courier.schemas.shipmentAddress import ShipmentAddressModelSchema
from app.fake_courier.schemas.shipmentProduct import ShipmentProductModelSchema


class ShipmentModelSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    UnitAmount: str = Field("3", min_length=1,
                            description="Ilość jednostek w wysyłce (zwykle waga dla typu jednostki=0)")
    Ref1: str = Field(uuid.uuid4().hex.upper()[0:12], max_length=25)
    Ref2: Optional[str] = Field(max_length=25)
    DeliveryRemark: str = Field(None, description="Uwaga dotycząca dostawy przesyłki!")
    CODValue: float = Field(120, description="Wartość za pobraniem (wykup)")
    CommissionType: int = Field(2, description="2 - Pozycja (musi mieć dostępne pozycje na magazynie)")
    Cosignee: ShipmentAddressModelSchema = Field({}, description="Adres")
    CODCurrency: int = Field(0, description="Rodzaj waluty płatności przy odbiorze: 0 - Domyślny (HRK) 1 - EUR")
    Commissions: List[ShipmentProductModelSchema] = Field([], description="Produkty")

    # Waluta. 0 HRK, 1 EUR
    @validator("CODCurrency")
    def validate_cod_currency(cls, codCurrency: int):
        if 0 <= codCurrency <= 1:
            return codCurrency
        return ValidationError("Validacija nije uspjela, provjerite potvrde za detalje!")


class ShipmentChangeStatusModelSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    tracking_no_from_cabroz: str = Field(uuid.uuid4().hex.upper()[0:12], description="tracking_no przesyłki z cabrozu")
    status_id: int = Field(71, description="Numer statusu")
