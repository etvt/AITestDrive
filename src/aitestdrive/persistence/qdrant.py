from typing import Any, List, Iterable

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams, VectorStruct

from aitestdrive.common.config import config


class QdrantService:
    __collection_name = 'aitestdrive-qdrant-collection'

    def __init__(self):
        self.__qdrant_client = AsyncQdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
        )

    async def search(self, query_vector: VectorStruct, limit: int) -> List[dict[str, Any]]:
        search_result = await self.__qdrant_client.search(
            collection_name=QdrantService.__collection_name,
            query_vector=query_vector,
            query_filter=None,
            limit=limit
        )
        return [hit.payload for hit in search_result]

    async def re_upload_collection(self,
                                   vector_size: int,
                                   vectors: Iterable[VectorStruct],
                                   payloads: Iterable[dict[str, Any]]):
        if QdrantService.__collection_name in await self.__get_collection_names():
            await self.__qdrant_client.delete_collection(QdrantService.__collection_name)

        await self.__qdrant_client.create_collection(
            collection_name=QdrantService.__collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

        self.__qdrant_client.upload_collection(
            collection_name=QdrantService.__collection_name,
            vectors=vectors,
            payload=payloads,
            ids=None,
            batch_size=256
        )

    async def __get_collection_names(self):
        collections = (await self.__qdrant_client.get_collections()).collections
        return map(lambda coll: coll.name, collections)


qdrant_service = QdrantService()
