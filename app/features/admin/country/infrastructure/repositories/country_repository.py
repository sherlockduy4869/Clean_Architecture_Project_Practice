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

from sqlalchemy.sql import func
import math


class CountryRepository(ICountryRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def get_all_countries(self, skip: int, limit: int) -> tuple[list[CountryEntity], int, int]:
        countries = self.session.query(CountryModel).offset(skip).limit(limit).all()

        total = self.session.query(func.count(CountryModel.id)).scalar() or 0

        total_pages = math.ceil(total / limit) if limit > 0 else 1

        result = (map_country_model_to_country_entity(country) for country in countries)
        return result, total, total_pages

    @override
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        result = (
            self.session.query(CountryModel)
            .filter(CountryModel.id == country_id)
            .first()
        )
        return map_country_model_to_country_entity(result)

    @override
    def create_country(self, country: CountryEntity) -> CountryEntity:
        country_model = map_country_entity_to_country_model(country)
        self.session.add(country_model)
        self.session.commit()
        return map_country_model_to_country_entity(country_model)

    @override
    def update_country(self, country_id: int, country: CountryEntity) -> CountryEntity:
        country_model = (
            self.session.query(CountryModel)
            .filter(CountryModel.id == country_id)
            .first()
        )
        # TODO: raise exception if country_model is None

        country_model = map_country_entity_to_country_model(country, country_model)
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
