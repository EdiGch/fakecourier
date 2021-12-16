from typing import Optional
from pydantic import BaseModel, Field
from faker import Faker

fake = Faker(['hr_HR'])


class ShipmentAddressModelSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    Name: str = Field(fake.name())
    CountryCode: str = Field('HR', max_length=2)
    Zipcode: str = Field(fake.postcode(), max_length=7)
    City: str = Field(fake.city())
    StreetAndNumber: str = Field(fake.street_address())
    Telephone: Optional[str] = Field(fake.phone_number())
    Fax: Optional[str] = Field(fake.phone_number())
    NotifyGSM: Optional[str] = Field(fake.phone_number())
    NotifyEmail: Optional[str] = Field(fake.ascii_email())
