from app.features.admin.country.application.interface.icountry_repository import (
    ICountryRepository,
)
from app.features.admin.country.domain.country_entity import CountryEntity


class CountryService:
    def __init__(self, country_repository: ICountryRepository):
        self.country_repository = country_repository

    def get_all_countries(self) -> list[CountryEntity]:
        return self.country_repository.get_all_countries()

    def get_country_by_id(self, country_id) -> CountryEntity:
        return self.country_repository.get_country_by_id(country_id)

    def create_country(self, country_data) -> CountryEntity:
        return self.country_repository.create_country(country_data)

    def update_country(self, country_id, country_data) -> CountryEntity:
        return self.country_repository.update_country(country_id, country_data)

    def delete_country(self, country_id) -> bool:
        return self.country_repository.delete_country(country_id)
