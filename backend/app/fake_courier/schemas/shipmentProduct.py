from pydantic import BaseModel, Field, validator, ValidationError
import uuid


class ShipmentProductModelSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    ItemCode: str = Field(uuid.uuid4().hex.upper()[0:6])
    Amount: int = 1

    @validator("Amount")
    def validate_amount(cls, amount: int):
        if amount != 0:
            return amount
        return ValidationError("Validacija nije uspjela, provjerite potvrde za detalje!")
