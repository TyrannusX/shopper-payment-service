from abc import ABC, abstractmethod
from domain import models
from pymongo.collection import ObjectId
from infrastructure import database


class CrudRepository(ABC):
    @abstractmethod
    async def create(self, model):
        pass

    @abstractmethod
    async def read(self, id):
        pass

    @abstractmethod
    async def read_all(self):
        pass

    @abstractmethod
    async def update(self, model):
        pass

    @abstractmethod
    async def delete(self, id):
        pass


class PaymentRepository(CrudRepository):
    async def create(self, model: models.Payment):
        bson = self.map_to_bson(model)
        inserted_id = database.collection.insert_one(bson).inserted_id
        return str(inserted_id)

    async def read(self, id):
        bson = database.collection.find_one({"_id": ObjectId(id)})
        model = self.map_to_domain(bson)
        return model

    async def read_all(self):
        return database.collection.find()

    async def update(self, model):
        bson = self.map_to_bson(model)
        database.collection.replace_one({"_id": bson["_id"]}, bson)

    async def delete(self, id):
        database.collection.delete_one({"_id": ObjectId(id)})

    def map_to_bson(self, model: models.Payment):
        bson = {
            "amount": model.amount,
            "status": model.status,
            "payment_processor_id": model.payment_processor_id,
            "payment_processor_status": model.payment_processor_status
        }

        if model.id:
            bson["_id"] = ObjectId(model.id)

        return bson

    def map_to_domain(self, bson):
        model = models.Payment()
        model.id = str(bson["_id"])
        model.amount = bson["amount"]
        model.status = bson["status"]
        model.payment_processor_id = bson["payment_processor_id"]
        model.payment_processor_status = bson["payment_processor_status"]

        return model
