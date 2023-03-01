from fastapi import FastAPI
import uvicorn

from app.core.config import settings
from app.api.endpoints import user

app = FastAPI(
    title=settings.PROJECT_NAME,
)
app.include_router(user.router, prefix='/users', tags=['Users'])


def main():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
