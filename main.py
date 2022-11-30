import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.v1 import stats
from core import config
from core.config import settings
from db import postgres

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    print(settings.DB_CONFIG)
    postgres.engine = create_async_engine(
        settings.DB_CONFIG,
        echo=True,
    )
    postgres.session = sessionmaker(
        postgres.engine, expire_on_commit=False, class_=AsyncSession
    )()
    await postgres.create_all()


@app.on_event('shutdown')
async def shutdown():
    await postgres.session.close()


app.include_router(stats.router, prefix='/api/v1/stats')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8010,
    )
