import asyncio
from contextlib import asynccontextmanager


class ReadWriteLock:

    @asynccontextmanager
    async def reader(self):
        await self.reader_acquire()
        try:
            yield
        finally:
            self.reader_release()

    @asynccontextmanager
    async def writer(self):
        await self.writer_acquire()
        try:
            yield
        finally:
            self.writer_release()

    def __init__(self):
        self.__readers = 0
        self.__write_in_progress: asyncio.Event | None = None
        self.__readers_done: asyncio.Event | None = None

    async def reader_acquire(self):
        if self.__write_in_progress is not None:
            await self.__write_in_progress.wait()

        self.__readers += 1

    def reader_release(self):
        self.__readers -= 1

        if (self.__readers == 0) and (self.__readers_done is not None):
            self.__readers_done.set()

    async def writer_acquire(self):
        self.__write_in_progress = asyncio.Event()

        if self.__readers > 0:
            self.__readers_done = asyncio.Event()
            await self.__readers_done.wait()

    def writer_release(self):
        if self.__readers_done is not None:
            self.__readers_done.set()
            self.__readers_done = None

        self.__write_in_progress.set()
        self.__write_in_progress = None
