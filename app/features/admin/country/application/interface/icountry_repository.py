from abc import ABC, abstractmethod

from app.features.admin.country.domain.country_entity import CountryEntity

class ICountryRepository(ABC):
    @abstractmethod
    def get_all_countries(self) -> list[CountryEntity]:
        pass

    @abstractmethod
    def get_country_by_id(self, country_id) -> CountryEntity:
        pass

    @abstractmethod
    def create_country(self, country_data) -> CountryEntity:
        pass

    @abstractmethod
    def update_country(self, country_id, country_data) -> CountryEntity:
        pass

    @abstractmethod
    def delete_country(self, country_id) -> bool:
        pass
