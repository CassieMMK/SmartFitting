from fastapi import FastAPI

from routers import body
from routers import clothes
from routers import tryon
from routers import recommendation

app = FastAPI()

app.include_router(body.router)
app.include_router(clothes.router)
app.include_router(tryon.router)
app.include_router(recommendation.router)