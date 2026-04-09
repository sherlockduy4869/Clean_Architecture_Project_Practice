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
from sqlalchemy import or_
import math

from sqlalchemy.exc import OperationalError, SQLAlchemyError, IntegrityError
from app.core.exceptions.repository import (
    ConnectionFailure,
    TransactionFailure,
    RepositoryException,
    UniqueConstraintFailure,
)

from app.core.exceptions.domain import (
    DomainException,
    NotFoundException,
    AlreadyExistsException,
)

from app.features.admin.country.domain.exceptions.exception import (
    CountryNotFoundException,
)

from typing import Optional


class CountryRepository(ICountryRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def get_all_countries(
        self, skip: int, limit: int, search: Optional[str] = None
    ) -> tuple[list[CountryEntity], int, int]:
        try:

            query = self.session.query(CountryModel)

            if search:
                pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        CountryModel.name.ilike(pattern),
                        CountryModel.country_code.ilike(pattern),
                        CountryModel.currency_code.ilike(pattern),
                    )
                )

            countries = (
                query.order_by(CountryModel.name.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )

            total = query.with_entities(func.count(CountryModel.id)).scalar() or 0

            total_pages = math.ceil(total / limit) if limit > 0 else 1

            result = (
                map_country_model_to_country_entity(country) for country in countries
            )
            return result, total, total_pages
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e

    @override
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        try:
            result = (
                self.session.query(CountryModel)
                .filter(CountryModel.id == country_id)
                .first()
            )

            if result is None:
                raise CountryNotFoundException(entity="Country", key=country_id)

            return map_country_model_to_country_entity(result)
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e

    @override
    def create_country(self, country: CountryEntity) -> CountryEntity:
        try:
            country_model = map_country_entity_to_country_model(country)
            self.session.add(country_model)
            self.session.commit()
            return map_country_model_to_country_entity(country_model)
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintFailure() from e
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e

    @override
    def update_country(self, country_id: int, country: CountryEntity) -> CountryEntity:
        try:
            country_model = (
                self.session.query(CountryModel)
                .filter(CountryModel.id == country_id)
                .first()
            )
            # TODO: raise exception if country_model is None

            country_model = map_country_entity_to_country_model(country, country_model)
            self.session.commit()
            return map_country_model_to_country_entity(country_model)
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintFailure() from e
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e

    @override
    def delete_country(self, country_id: int) -> bool:
        try:
            country_model = (
                self.session.query(CountryModel)
                .filter(CountryModel.id == country_id)
                .first()
            )

            if country_model is None:
                raise CountryNotFoundException(entity="Country", key=country_id)

            self.session.delete(country_model)
            self.session.commit()
            return True
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TransactionFailure() from e
