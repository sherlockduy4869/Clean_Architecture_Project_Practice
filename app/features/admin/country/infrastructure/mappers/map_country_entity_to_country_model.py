from typing import Optional
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.infrastructure.models.country_model import CountryModel
from sqlalchemy import inspect
from sqlalchemy.orm import Mapper

def map_country_entity_to_country_model(
    country_entity: CountryEntity, model: Optional[CountryModel] = None
) -> CountryModel:
    """
    Maps a CountryEntity to a CountryModel.

    Args:
        country_entity (CountryEntity): The CountryEntity instance to be mapped.
    Returns:
        CountryModel: The mapped CountryModel instance.
    """

    if model is not None:
        return CountryModel(
            id=model.id,
            name=country_entity.name,
            country_code=country_entity.country_code,
            currency_code=country_entity.currency_code,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
   
    mapper: Mapper[CountryModel] = inspect((CountryModel))
    column_names = [cols.key for cols in mapper.column_attrs]

    primary_key = [cols.key for cols in mapper.primary_key]

    skip = primary_key + ["created_at", "updated_at"]

    for column in column_names:
        if column in skip:
            continue
        if hasattr(country_entity, column):
            value = getattr(country_entity, column)
            if value is not None:
                setattr(model, column, value)
    
    return model