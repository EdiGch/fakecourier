from pydantic import BaseModel


class ShipmentStatusModelSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    status_code: int = 8
    shipment_id: int = 1
