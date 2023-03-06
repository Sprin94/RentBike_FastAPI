from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload


from app.db.crud.base import BaseCrud
from app.db.models.bike import Bike, BikeModel
from app.db.models.order import Order
from app.db.schemas.bike import BikeCreate, BikeModelCreate


class BikeCrud(BaseCrud):
    async def get_all_bikes(self) -> list[Bike]:
        stmt = (select(Bike).join(BikeModel))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_bike(self, bike: BikeCreate) -> Bike:
        bike = Bike(**bike.dict())
        self.session.add(bike)
        await self.session.commit()
        await self.session.refresh(bike)
        return bike

    async def get_available_bikes(
            self,
            date_rent_start: date,
            date_rent_end: date,
            bike_model: str,
            ):

        stmt = (select(
                    Bike.number,
                    BikeModel.model,
                    Bike.color,
                    Bike.mileage,
                    Bike.cost_per_day,
                    Bike.photo,
                    Bike.born_year,
                    )
                .join(BikeModel)
                .where(
                    and_(~Bike.orders.any(
                        and_(Order.date_end >= date_rent_start,
                             Order.date_begin <= date_rent_end)
                        ),
                        Bike.model.has(model=bike_model),
                        Bike.status == 'available',
                    ))

                )

        result = await self.session.execute(stmt)
        available_bikes = result.mappings().all()
        return available_bikes


class BikeModelCrud(BaseCrud):
    async def create_model(self, model: BikeModelCreate):
        model = BikeModel(**model.dict())
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.__dict__
