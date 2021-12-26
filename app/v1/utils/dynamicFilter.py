from sqlalchemy.orm import Session
from typing import Optional

def dynamic_filters(model, query: Session, filters: dict) -> Optional[Session]:

    for attr, value in filters.items():
      query = query.filter(getattr(model, attr) == value)

    return query