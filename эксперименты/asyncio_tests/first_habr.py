# coding: utf-8
"""https://habr.com/ru/post/337420/ ."""
import asyncio


async def foo() -> None:
    """Корутина."""
    print('Running in foo')
    await asyncio.sleep(0)
    print('Explicit context switch to foo again')


async def bar() -> None:
    """Корутина."""
    print('Explicit context to bar')
    await asyncio.sleep(0)
    print('Implicit context switch back to bar')


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()

# * Сначала мы объявили пару простейших корутин, которые притворяются неблокирующими, используя sleep из asyncio
# * Корутины могут быть запущены только из другой корутины, или обёрнуты в задачу с помощью create_task
# * После того, как у нас оказались 2 задачи, объединим их, используя wait
# * И, наконец, отправим на выполнение в цикл событий через run_until_complete

# Используя await в какой-либо корутине, мы таким образом объявляем,
# что корутина может отдавать управление обратно в event loop, который,
# в свою очередь, запустит какую-либо следующую задачу: bar.
# В bar произойдёт тоже самое: на await asyncio.sleep управление будет передано обратно в цикл событий,
# который в нужное время вернётся к выполнению foo.
