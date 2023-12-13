__singletons = {
}


def get(constructor):
    return __singletons[constructor]


def of(constructor):
    async def async_dep():
        instance = __singletons.get(constructor, None)
        if not instance:
            instance = constructor()
            __singletons[constructor] = instance
        return instance

    return async_dep
