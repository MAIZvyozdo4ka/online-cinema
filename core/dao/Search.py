import asyncio
from elasticsearch import AsyncElasticsearch

class Search:
    client = AsyncElasticsearch(
        api_key='Tkhycl9wTUI0UWs4V3FEM240Y0o6OXV3OEEzY01TT2E4eEpDdDl6MjRBZw==',
        cloud_id='744838197d8a4a898c1f01d378506c48:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGU1ODNlZWVhODAyMzQ3YmQ5NzlkMzBhZDc2YzMwMjE2JDhiMTU3ZjM5YjdmMTRkYjVhYTQyMGM5ZDgzODI3YTI3'
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