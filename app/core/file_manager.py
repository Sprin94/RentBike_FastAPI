import os

from app.core.config import settings


def init_media_dirs():
    if not os.path.exists(settings.MEDIA_DIR):
        os.makedirs(settings.MEDIA_DIR)
    for dirs in settings.DIRS:
        new_dirs = os.path.join(settings.MEDIA_DIR, dirs)
        if not os.path.exists(new_dirs):
            os.makedirs(new_dirs)


async def save_bike_photo(bike_number: str, photo):
    contents = await photo.read()
    format = photo.filename.split('.')[-1]
    filename = f'{bike_number}.{format}'
    path = f"{settings.MEDIA_DIR}/bikes_photo/{filename}"
    with open(path, "wb") as f:
        f.write(contents)
    return path
