from motor.core import Collection
from motor.motor_asyncio import AsyncIOMotorClient


class DataStorage(object):
    def __init__(self, database='test'):
        self._client = AsyncIOMotorClient()
        self._db = self._client[database]

    async def get_roads(self) -> list:
        sections = await self._entities(self._db.sections)
        return self._unique((section['road'] for section in sections))

    async def get_section(self, identifier: str) -> dict:
        return await self._db.sections.find_one({'id': identifier})

    async def put_section(self, identifier: str, section: dict):
        await self._db.sections.find_one_and_replace(
            {'id': identifier}, section, upsert=True
        )

    async def remove_section(self, identifier: str):
        self._db.sections.delete_one({'id': identifier})

    async def get_repairs(self, road: str, begin=0, end=0) -> list:
        query = {
            'road': road,
        }

        if begin:
            query['begin'] = str(begin)

        if end:
            query['end'] = str(end)

        return await self._entities(self._db.repairs, query)

    async def get_repair(self, identifier: str) -> dict:
        return await self._db.repairs.find_one({'id': identifier})

    async def put_repair(self, identifier: str, repair: dict):
        await self._db.repairs.find_one_and_replace(
            {'id': identifier}, repair, upsert=True
        )

    async def remove_repair(self, identifier: str):
        self._db.repairs.delete_one({'id': identifier})

    async def get_locations(self) -> list:
        return await self._entities(self._db.locations)

    async def put_location(self, identifier: str, location: dict):
        await self._db.locations.find_one_and_replace(
            {'id': identifier}, location, upsert=True
        )

    async def remove_location(self, identifier: str):
        self._db.locations.delete_one({'id': identifier})

    @staticmethod
    def _pure_entity(entity: dict) -> dict:
        entity.pop('_id')
        return entity

    @staticmethod
    async def _entities(collection: Collection, query=None) -> list:
        return [
            DataStorage._pure_entity(entity)
            for entity in await collection.find(query).to_list(None)
        ]

    @staticmethod
    def _unique(collection) -> list:
        return list(set(collection))

