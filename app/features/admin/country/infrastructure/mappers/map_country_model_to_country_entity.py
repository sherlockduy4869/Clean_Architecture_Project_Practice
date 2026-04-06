from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.infrastructure.models.country_model import CountryModel


def map_country_model_to_country_entity(country_model: CountryModel) -> CountryEntity:

    """
    Maps a CountryModel to a CountryEntity.
    
    Args:
        country_model (CountryModel): The CountryModel instance to be mapped.
    Returns:
        CountryEntity: The mapped CountryEntity instance.
    """

    return CountryEntity(
        id = country_model.id,
        name = country_model.name,
        country_code = country_model.country_code,
        currency_code = country_model.currency_code,
        created_at = country_model.created_at,
        updated_at = country_model.updated_at
    )