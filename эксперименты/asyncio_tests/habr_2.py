# coding: utf-8
"""https://habr.com/ru/post/337420/ ."""
import asyncio
import time


start = time.time()


def tic() -> str:
    """Возвращает временную разнницу от начала запуска скрипта."""
    return 'at %1.1f seconds' % (time.time() - start)


async def gr1() -> str:
    """Busy waits for a second, but we don't want to stick around..."""
    print('gr1 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr1 ended work: {}'.format(tic()))


async def gr2() -> str:
    """Busy waits for a second, but we don't want to stick around..."""
    print('gr2 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr2 Ended work: {}'.format(tic()))


async def gr3() -> str:
    """Let's do some stuff."""
    print("Let's do some stuff while the coroutines are blocked, {}".format(tic()))
    await asyncio.sleep(1)
    print("Done!")


ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(gr1()),
    ioloop.create_task(gr2()),
    ioloop.create_task(gr3()),
]
ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.close()
