from typing import override

from sqlalchemy.orm import Session

from app.features.admin.country.application.interface.icountry_repository import (
    ICountryRepository,
)
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.infrastructure.models.country_model import CountryModel
from app.features.admin.country.infrastructure.mappers.map_country_entity_to_country_model import (
    map_country_entity_to_country_model,
)
from app.features.admin.country.infrastructure.mappers.map_country_model_to_country_entity import (
    map_country_model_to_country_entity,
)


class CountryRepository(ICountryRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def get_all_countries(self) -> list[CountryEntity]:
        countries = self.session.query(CountryModel).all()
        result = (map_country_model_to_country_entity(country) for country in countries)
        return result

    @override
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        result = (
            self.session.query(CountryModel)
            .filter(CountryModel.id == country_id)
            .first()
        )
        return result

    @override
    def create_country(self, country: CountryEntity) -> CountryEntity:
        country_model = map_country_entity_to_country_model(country)
        result = self.session.add(country_model)
        self.session.commit()
        return map_country_model_to_country_entity(result)

    @override
    def update_country(self, country_id: int, country: CountryEntity) -> CountryEntity:
        country_model = (
            self.session.query(CountryModel)
            .filter(CountryModel.id == country_id)
            .first()
        )
        # TODO: raise exception if country_model is None

        country_model = map_country_entity_to_country_model(country)
        self.session.update(country_model)
        self.session.commit()
        return map_country_model_to_country_entity(country_model)

    @override
    def delete_country(self, country_id: int) -> bool:
        country_model = (
            self.session.query(CountryModel)
            .filter(CountryModel.id == country_id)
            .first()
        )
        # TODO: raise exception if country_model is None
        self.session.delete(country_model)
        self.session.commit()
        return True
