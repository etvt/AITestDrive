from aitestdrive.persistence.qdrant import QdrantService

__singletons = {
    QdrantService: QdrantService()
}


def get(clazz):
    return __singletons[clazz]


def depends(clazz):
    async def async_dep():
        return get(clazz)

    return async_dep
