from fastapi import FastAPI

from trainr.api.v1 import v1
from trainr.api.v1.models.health import Health

app = FastAPI()

app.include_router(v1, prefix='/api')


@app.get("/", response_model=Health)
async def root():
    return Health(healthy=True)
