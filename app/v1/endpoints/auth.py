from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PassowrdRequestForm
from sqlalchemy.orm import Session

from app.v1.database import get_db

router = APIRouter()

@router.post("/login", include_in_schema=False)
async def login(
    from_data: OAuth2PassowrdRequestForm = Depends(), db: Session = Depends(get_db)
):
    
    return 