from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.crud.bike import BikeCrud, BikeModelCrud
from app.db.schemas.bike import BikeCreate, BikeInDB, BikeModelInDB, BikeModelCreate


router = APIRouter()


# @router.get('', response_model=list[BikeInDB])
# async def get_all_bike(crud: BikeCrud = Depends()):
#     bikes = await crud.get_all_bikes()
#     return bikes


@router.get('', response_model=list[BikeInDB])
async def get_available_bike(
    date_rent_start: date,
    date_rent_finish: date,
    model: str,
    crud: BikeCrud = Depends()
):
    bikes = await crud.get_available_bikes(
        date_rent_start,
        date_rent_finish,
        model)
    return bikes


@router.post('/add-bike', response_model=BikeInDB)
async def create_bike(
    bike: BikeCreate,
    crud: BikeCrud = Depends()
):
    result = await crud.create_bike(bike)
    return result


@router.post('/add-bike-model', response_model=BikeModelInDB)
async def create_bike_model(
    model: BikeModelCreate,
    crud: BikeModelCrud = Depends()
):
    result = await crud.create_model(model)
    return result
