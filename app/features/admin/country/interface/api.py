from typing import Annotated
from fastapi import Depends, Query, status
from app.core.router.router import get_versioned_router
from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.interface.dependencies import get_country_service
from app.features.admin.country.interface.schemas import (
    CountryListResponse,
    CountryResponse,
    CreateCountryRequest,
    UpdateCountryRequest,
    PaginationMeta,
)
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.interface.mappers.map_create_country_schema_to_entity import (
    mapCreateCountryRequestToEntity,
)

from app.features.admin.country.interface.mappers.map_update_country_schema_to_entity import (
    mapUpdateCountryRequestToEntity,
)

from typing import Optional

v1_router = get_versioned_router("v1")


@v1_router.get("/admin/countries", status_code=status.HTTP_200_OK)
def get_countries(
    country_service: Annotated[CountryService, Depends(get_country_service)],
    skip: Annotated[
        int, Query(ge=1, description="Page number should be greater than or equal to 1")
    ] = 1,
    limit: Annotated[
        int,
        Query(
            ge=1,
            description="Number of items per page should be greater than or equal to 1",
        ),
    ] = 10,
    search: Annotated[
        Optional[str],
        Query(
            description="Search term for filtering countries by name, code, or currency code",
        ),
    ] = None,
) -> CountryListResponse:
    result, total, total_pages = country_service.get_all_countries(skip - 1, limit, search)

    meta: PaginationMeta = PaginationMeta(
        total=total, total_pages=total_pages, page_size=limit, current_page=skip
    )

    return CountryListResponse(status="success", data=result, meta=meta)


@v1_router.get("/admin/countries/{country_id}", status_code=status.HTTP_200_OK)
def get_country_by_id(
    country_id: int,
    country_service: Annotated[CountryService, Depends(get_country_service)],
) -> CountryResponse:
    result = country_service.get_country_by_id(country_id)
    return CountryResponse(status="success", data=result)


@v1_router.post("/admin/countries", status_code=status.HTTP_201_CREATED)
def create_country(
    data: CreateCountryRequest,
    country_service: Annotated[CountryService, Depends(get_country_service)],
) -> CountryResponse:

    country_entity = mapCreateCountryRequestToEntity(data)

    result = country_service.create_country(country_entity)
    return CountryResponse(status="success", data=result)


@v1_router.patch("/admin/countries/{country_id}", status_code=status.HTTP_200_OK)
def patch_country(
    country_id: int,
    data: UpdateCountryRequest,
    country_service: Annotated[CountryService, Depends(get_country_service)],
) -> CountryResponse:
    country_entity = mapUpdateCountryRequestToEntity(data)
    result = country_service.update_country(country_id, country_entity)
    return CountryResponse(status="success", data=result)


@v1_router.delete(
    "/admin/countries/{country_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_country(
    country_id: int,
    country_service: Annotated[CountryService, Depends(get_country_service)],
) -> None:
    country_service.delete_country(country_id)
    # return CountryResponse(status="success", data=None)
