from typing import Optional, List, Any, Dict

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Query, joinedload
from sqlalchemy import select


@as_declarative()
class Base:
    NON_UPDATABLE_FIELDS = ["_sa_instance_state", "id"]

    @classmethod
    def get_updatable_fields(cls, entity: Any) -> dict:
        return {k: v for (k, v) in vars(entity).items() if k not in cls.NON_UPDATABLE_FIELDS}

    @classmethod
    def get_updatable_fields_from_dict(cls, entity: Dict) -> dict:
        return {k: v for (k, v) in entity.items() if k not in cls.NON_UPDATABLE_FIELDS}

    @classmethod
    def get_configured_query(cls, options: Optional[List]) -> Query:
        query = select(cls)
        if options is not None:
            for option in options:
                query = query.options(joinedload(option))

        if hasattr(cls, "is_deleted"):
            query = query.filter_by(is_deleted=False)

        return query
