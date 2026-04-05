import asyncio
from random import random
from config import log
import time

"""
O Problema: Um Producer coloca 10 números em uma asyncio.Queue. Um Consumer retira esses números para processar.

1.  O Consumer deve ter um timeout de 2 segundos para cada item.
2.  Simule que, se o número for "7", o processamento demora 5 segundos (causando um estouro de timeout).
3.  Seu código deve capturar a exceção de timeout, avisar que o "Item 7 falhou" e continuar processando o restante da fila sem travar o programa.
"""

QUEUE_SIZE = 10
MAX_CONSUMERS = 2


async def producer(queue: asyncio.Queue):
    for i in range(QUEUE_SIZE):
        await queue.put({"retries": 0, "data": i})
        await asyncio.sleep(.1)
        log.debug(f"elemento {i} adicionado.")
    

async def process(item: dict):
    if item["data"] == 7:
        await asyncio.sleep(5)
    elif item["data"] == 9:
        await asyncio.sleep(9)
    else:
        await asyncio.sleep(random())


async def consumer(consumer: str, queue: asyncio.Queue, error_queue: asyncio.Queue):
    try:
        while True:
            item = await queue.get()
            TIMEOUT = 2 ** item["retries"]
            try:
                async with asyncio.timeout(TIMEOUT):
                    start = time.perf_counter()
                    await process(item)
                    log.debug(
                        f"{consumer} -> {item['data']} processado em {str(time.perf_counter() - start)[:4]}s -- {item['retries']} tentativas"
                    )
            except asyncio.TimeoutError:
                item["retries"] += 1
                if item["retries"] <= 3:
                    await queue.put(item)
                    log.error(
                        f"{consumer} -> {item['data']} timeout -- {item['retries']}"
                    )
                else:
                    await error_queue.put(item)
                    log.critical(f"{consumer} -> {item['data']} falhou definitivamente")
            finally:
                queue.task_done()
    except asyncio.CancelledError:
        await asyncio.sleep(random())
        log.warning(f"consumer {consumer} encerrado.")
        raise


async def main():
    queue = asyncio.Queue()  # consumer queue
    error_queue = asyncio.Queue()  # error queue

    log.info("producer adicionando elementos na fila\n")
    await producer(queue)
    print("\n")
    await asyncio.sleep(1)

    log.info("iniciando processamento com consumers\n")
    tasks = [
        asyncio.create_task(consumer(f"C{n}", queue, error_queue))
        for n in range(MAX_CONSUMERS)
    ]

    await error_queue.join()
    await queue.join()

    await asyncio.sleep(1)
    log.info("graceful shutdown dos consumers")
    for t in tasks:
        t.cancel()

    res = await asyncio.gather(*tasks, return_exceptions=True)

    for i, r in enumerate(res):
        if not isinstance(r, asyncio.CancelledError):
            log.critical(f"erro inesperado ao processar C{i}")

    log.info("consumer loop finalizado.")


if __name__ == "__main__":
    log.info("Teste de producer/consumer iniciado\n")
    time.sleep(1)
    asyncio.run(main())
    time.sleep(1)
    print("\n")
    log.info("Teste de producer/consumer finalizado")
