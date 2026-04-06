import time
import asyncio


async def f(r: str, t: float) -> str:
    print(f"Running {r}")
    await asyncio.sleep(t)
    print(f"{r} finished")
    return r


async def main():
    res = await asyncio.gather(
        f("A",1),
        f("B",2),
        f("C",3)
    )

    print(res)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    print(f"Tempo de execucao: {time.perf_counter() - start}")
