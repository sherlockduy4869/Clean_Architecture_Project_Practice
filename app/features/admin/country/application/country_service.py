from app.features.admin.country.application.interface.icountry_repository import (
    ICountryRepository,
)
from app.features.admin.country.domain.country_entity import CountryEntity
from app.core.exceptions.repository import (
    UniqueConstraintFailure,
)

from app.features.admin.country.domain.exceptions.exception import (
    CountryAlreadyExistsException,
)

from typing import Optional

class CountryService:
    def __init__(self, country_repository: ICountryRepository):
        self.country_repository = country_repository

    def get_all_countries(self, skip: int, limit: int, search: Optional[str] = None) -> tuple[list[CountryEntity], int, int]:
        return self.country_repository.get_all_countries(skip, limit, search)

    def get_country_by_id(self, country_id) -> CountryEntity:
        return self.country_repository.get_country_by_id(country_id)

    def create_country(self, country_data) -> CountryEntity:
        try:
            return self.country_repository.create_country(country_data)
        except UniqueConstraintFailure:
            raise CountryAlreadyExistsException(entity="Country", key=country_data.name)

    def update_country(self, country_id, country_data) -> CountryEntity:
        try:
            return self.country_repository.update_country(country_id, country_data)
        except UniqueConstraintFailure:
            raise CountryAlreadyExistsException(entity="Country", key=country_data.name)

    def delete_country(self, country_id) -> bool:
        return self.country_repository.delete_country(country_id)
