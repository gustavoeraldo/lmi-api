from fastapi import APIRouter

from .endpoints import measurements, users, measureTypes

api_router = APIRouter()
api_router.include_router(users.router, prefix='/lmi/users', tags=['users'])
api_router.include_router(measurements.router, prefix="/lmi/measurements", tags=["measurements"])
api_router.include_router(measureTypes.router, prefix='/lmi/mesure-types', tags=['mesure-types'])
