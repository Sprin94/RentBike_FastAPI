from fastapi import FastAPI
import uvicorn

from app.core.file_manager import init_media_dirs
from app.core.config import settings
from app.api.endpoints import auth, user, bike, order

app = FastAPI(
    title=settings.PROJECT_NAME,
)
app.include_router(user.router, prefix='/users', tags=['Users'])
app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(bike.router, prefix='/bikes', tags=['Bike'])
app.include_router(order.router, prefix='/orders', tags=['Order'])


@app.on_event("startup")
async def db_load():
    init_media_dirs()


def main():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
