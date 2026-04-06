import asyncio
from string import ascii_uppercase


async def worker(w: str, q: asyncio.Queue):
    try:
        while True:
            t = await q.get()
            print(f"Processing {w} in {t}")
            await asyncio.sleep(0.5)
            q.task_done()
            print(f"Finished {w}")
    except asyncio.CancelledError:
        print("Worker morto.")


async def main():
    MAX_SIZE = 26

    q = asyncio.Queue()
    for i in ascii_uppercase:
        await q.put(i)

    tasks = [asyncio.create_task(worker(f"W-{i}", q)) for i in range(1, MAX_SIZE + 1)]

    await q.join()

    print("Graceful shutdown dos workers:")
    for t in tasks:
        t.cancel()

    asyncio.gather(*tasks)
    print("Worker loop finalizado")


if __name__ == "__main__":
    asyncio.run(main())
