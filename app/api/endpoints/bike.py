from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File

from app.db.models.user import User
from app.db.crud.bike import BikeCrud, BikeModelCrud
from app.db.schemas.bike import (BikeCreate, BikeInDB, BikeModelInDB,
                                 BikeModelCreate, BikeUpdate, BikeBase)
from app.api.utils.security import get_current_active_superuser
from app.core.config import settings
from app.core.file_manager import save_bike_photo

router = APIRouter()


@router.get('/', response_model=list[BikeInDB])
async def get_all_bike(
    crud: BikeCrud = Depends(),
    admin: User = Depends(get_current_active_superuser),
):
    bikes = await crud.get_all_bikes()
    return bikes


@router.get('/available', response_model=list[BikeInDB])
async def get_available_bike(
    date_rent_start: date,
    date_rent_finish: date,
    model: str,
    crud: BikeCrud = Depends(),
):
    bikes = await crud.get_available_bikes(
        date_rent_start,
        date_rent_finish,
        model)
    return bikes


@router.get('/{bike_number}', response_model=BikeInDB)
async def get_bike(
    bike_number: str,
    crud: BikeCrud = Depends(),
    admin: User = Depends(get_current_active_superuser),
):
    result = await crud.get_bike(bike_number)
    return result


@router.post('/', response_model=BikeInDB)
async def create_bike(
    bike: BikeCreate,
    photo: UploadFile = File(None),
    crud: BikeCrud = Depends(),
    admin: User = Depends(get_current_active_superuser),
):
    if photo:
        path_photo = save_bike_photo(bike.number, photo)
        bike.photo = path_photo
    result = await crud.create_bike(bike)
    return result


@router.patch('/{bike_number}', response_model=BikeBase)
async def update_bike(
    bike_number: str,
    bike: BikeUpdate = BikeUpdate(),
    photo: UploadFile = File(None),
    crud: BikeCrud = Depends(),
    admin: User = Depends(get_current_active_superuser),
):
    if photo:
        path_photo = await save_bike_photo(bike_number, photo)
        bike.photo = path_photo
    result = await crud.update_bike(bike_number, bike)
    return result


@router.post(
        '/add-bike-model',
        response_model=BikeModelInDB,
        )
async def create_bike_model(
    model: BikeModelCreate,
    crud: BikeModelCrud = Depends(),
    admin: User = Depends(get_current_active_superuser),
):
    result = await crud.create_model(model)
    return result
