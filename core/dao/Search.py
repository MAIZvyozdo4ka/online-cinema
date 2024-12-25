import asyncio
from elasticsearch import AsyncElasticsearch
from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname


class ESSettings(BaseSettings):
    API_KEY : str
    CLOUD_ID : str
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(dirname(abspath(__file__))) + '/env/search.env',
        frozen = True
    )


settings = ESSettings()


class Search:
    client = AsyncElasticsearch(
        api_key=settings.API_KEY,
        cloud_id=settings.CLOUD_ID
    )

    async def search(self, text):
        res = await self.client.search(index="film_index", query={
            "match": {
                "description": text
            }
        })

        ans = []
        for i in res['hits']['hits']:
            ans += [int(i['_id'])]

        return ans

    async def delete(self, index):
        await self.client.delete(index="film_index", id=index)

    async def add(self, index, discr):
        await self.client.index(
            index="film_index",
            id=index,
            document={
                "description": discr,
            }
        )

    async def update(self, index, discr):
        await self.delete(index)
        await self.add(index, discr)

    async def close(self):
        await self.client.close()