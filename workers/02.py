import asyncio
from string import ascii_uppercase
from random import random


async def process(thing):
    print(f"Processing thing: {thing}")
    await asyncio.sleep(random())
    print(f"{thing} ended processing")


async def worker(i: int, sem: asyncio.Semaphore, q: asyncio.Queue):
    try:
        while True:
            print(f"Worker {i}")
            t = await q.get()
            try:
                async with sem:
                    await process(t)
            except Exception as e:
                print(f"Worker {i} nao conseguiu processar {t}: {e}")
            finally:
                q.task_done()
    except asyncio.CancelledError:
        print(f"Worker finalizado {i}.")


async def main():
    MAX_SIZE = 5

    q = asyncio.Queue()
    for letter in ascii_uppercase:
        await q.put(letter)

    sem = asyncio.Semaphore(MAX_SIZE)
    tasks = [
        asyncio.create_task(worker(i, sem, q)) for i in range(1, (MAX_SIZE * 2) + 1)
    ]
    await q.join()

    for t in tasks:
        t.cancel()

    asyncio.gather(*tasks, return_exceptions=True)
    print("Tasks finalizadas")


if __name__ == "__main__":
    asyncio.run(main())
