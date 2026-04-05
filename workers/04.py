import asyncio
from random import random
from config import log

"""
O Problema: Um Producer coloca 10 números em uma asyncio.Queue. Um Consumer retira esses números para processar.

1.  O Consumer deve ter um timeout de 2 segundos para cada item.
2.  Simule que, se o número for "7", o processamento demora 5 segundos (causando um estouro de timeout).
3.  Seu código deve capturar a exceção de timeout, avisar que o "Item 7 falhou" e continuar processando o restante da fila sem travar o programa.
"""

QUEUE_SIZE = 100
MAX_CONSUMERS = 10


async def producer(q: asyncio.Queue):
    log.debug("producer adicionando elementos na fila")
    for i in range(QUEUE_SIZE):
        await q.put({"retries": 0, "data": i})


async def process(item: dict):
    log.debug(f"Processando {item['data']} -- tentativa {item['retries']}")
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
                    await process(item)
                    log.debug(f"item {item['data']} processado em consumer {consumer}")
            except asyncio.TimeoutError:
                item["retries"] += 1
                if item["retries"] <= 3:
                    await queue.put(item)
                    log.error(
                        f"erro de timeout ao processar {item['data']} em {consumer}"
                    )
                else:
                    await error_queue.put(item)
                    log.critical(
                        f"item {item['data']} falhou definitivamente no consumer {consumer}"
                    )
            finally:
                queue.task_done()
    except asyncio.CancelledError:
        log.warning(f"consumer {consumer} encerrado.")
        raise


async def main():
    queue = asyncio.Queue()  # consumer queue
    error_queue = asyncio.Queue()  # error queue
    await producer(queue)

    tasks = [
        asyncio.create_task(consumer(f"C{n}", queue, error_queue))
        for n in range(MAX_CONSUMERS)
    ]

    await error_queue.join()
    await queue.join()

    log.info("graceful shutdown dos consumers")
    for t in tasks:
        t.cancel()

    res = await asyncio.gather(*tasks, return_exceptions=True)

    for i, r in enumerate(res):
        if not isinstance(r, asyncio.CancelledError):
            log.critical(f"erro inesperado ao processar C{i}")

    log.info("consumer loop finalizado.")


if __name__ == "__main__":
    log.info("Teste de producer/consumer iniciado")
    asyncio.run(main())
    log.info("Teste de producer/consumer finalizado")
