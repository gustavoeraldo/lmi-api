from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse
from dotenv import find_dotenv, load_dotenv
import os
import uvicorn

from app.v1.router import api_router # Use this line for deployment
from app.v1.database.mainDB import SessionLocal

load_dotenv(find_dotenv())

origins = os.getenv("ORIGINS")

app = FastAPI(
    title='LMI API',
    description='Manage data from LMI Lab researches.',
    redoc_url=None,
    root_path='/',
    version='1.0.0',

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/docs', include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='LMI API'
    )

@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(api_router)

@app.get('/', include_in_schema=False)
def home():
    return RedirectResponse(url='/docs') 

if __name__ == '__main__':
    uvicorn.run(app)