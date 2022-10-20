from app.imports import UUID, Column, as_declarative


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True))
