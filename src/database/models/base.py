from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def to_dict(self, include_relations: bool = False) -> dict:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if include_relations:
            for attr in self.__mapper__.relationships:
                relation = getattr(self, attr.key)
                if relation is not None:
                    if isinstance(relation, list):
                        data[attr.key] = [item.to_dict() for item in relation]
                    else:
                        data[attr.key] = relation.to_dict()
        return data
