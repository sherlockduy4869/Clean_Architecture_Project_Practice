from pydantic import BaseModel
from app.features.admin.country.domain.country_entity import CountryEntity

class CreateCountryRequest(BaseModel):
    name: str
    country_code: str
    currency_code: str


class CountryListResponse(BaseModel):
    status: str
    data: list[CountryEntity]

class CountryResponse(BaseModel):
    status: str
    data: CountryEntity
