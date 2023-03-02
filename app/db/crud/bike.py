from sqlalchemy import select


from app.db.crud.base import BaseCrud
from app.db.models.bike import Bike, BikeModel
from app.db.schemas.bike import BikeCreate, BikeModelCreate


class BikeCrud(BaseCrud):
    async def get_all_bikes(self) -> list[Bike]:
        stmt = (select(Bike).join(BikeModel))
        result = await self.session.execute(stmt)
        return result.all()

    async def create_bike(self, bike: BikeCreate) -> Bike:
        bike = Bike(**bike.dict())
        self.session.add(bike)
        await self.session.commit()
        await self.session.refresh(bike)
        return bike


class BikeModelCrud(BaseCrud):
    async def create_model(self, model: BikeModelCreate):
        model = BikeModel(**model.dict())
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.__dict__
