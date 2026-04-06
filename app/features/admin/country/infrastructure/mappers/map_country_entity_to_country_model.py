
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.infrastructure.models.country_model import CountryModel


def map_country_entity_to_country_model(country_entity: CountryEntity) -> CountryModel:

    """
    Maps a CountryEntity to a CountryModel.
    
    Args:
        country_entity (CountryEntity): The CountryEntity instance to be mapped.
    Returns:
        CountryModel: The mapped CountryModel instance.
    """

    return CountryModel(
        id = country_entity.id,
        name = country_entity.name,
        country_code = country_entity.country_code,
        currency_code = country_entity.currency_code,
        created_at = country_entity.created_at,
        updated_at = country_entity.updated_at
    )