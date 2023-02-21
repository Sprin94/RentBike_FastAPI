from fastapi import FastAPI
import uvicorn

from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)


def main():
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
