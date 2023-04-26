from typing import Any
from src.domain.entities.base import Base


async def model_to_dict(model: Base,
                        convert_to_str: bool = False) -> dict[str, Any]:
    return {c.name: str(getattr(model, c.name)) if convert_to_str else
            getattr(model, c.name) for c in model.__table__.columns}
