import asyncio
from typing import Callable, Awaitable, Any

from config import log

# import numpy as np
# import pandas as pd

"""
DESAFIO: EVOLUÇÃO PARA ARQUITETURA ORIENTADA A EVENTOS (PUB/SUB)

Meta: Refatorar este sistema de fila única (Point-to-Point) em memória para simular 
os pilares de um broker de mensagens (como Kafka) e microsserviços resilientes.

Etapas de Implementação:
1. Fan-out (Pub/Sub): Criar um `EventBus` que receba mensagens em "tópicos" e faça o 
   broadcast (cópias) para múltiplas filas inscritas simultaneamente.
2. Partições e Ordem: Adicionar uma "chave de roteamento" nas mensagens (ex: user_id) 
   e usar um algoritmo de hash para garantir que eventos de uma mesma chave sejam processados 
   sempre pela mesma fila e consumidor, mantendo a ordem.
3. Idempotência: Implementar um banco de dados em memória (`fake_db`). Forçar falhas 
   no consumidor antes do `task_done()` e implementar validação por ID para garantir 
   que mensagens reentregues não alterem o estado de forma duplicada.
4. Coreografia (Padrão Saga): Criar dois "serviços" independentes (ex: Pedido e Pagamento) 
   que se comunicam puramente reagindo aos eventos do EventBus, incluindo o disparo de 
   eventos de compensação (rollback) em caso de falha no fluxo.
"""


class Events:
   _topics: dict[str, set[Callable[..., Awaitable[Any]]]] = {}

   @classmethod
   def get_topics(cls) -> dict[str, set[Callable[..., Awaitable[Any]]]]:
      return cls._topics

   @classmethod
   def get_keys(cls):
      return cls._topics.keys()

   @classmethod
   def subscribe(cls, topic: str, callback: Callable[..., Awaitable[Any]]) -> None:
      if topic not in cls._topics:
         cls._topics[topic] = set()
      cls._topics[topic].add(callback)

   @classmethod
   def unsubscribe(cls, topic: str, callback: Callable[..., Awaitable[Any]]) -> None:
      if topic in cls._topics:
         cls._topics[topic].discard(callback)

async def test():
   log.info("Teste")

async def main():
   Events.subscribe("teste", test)

   log.info("Tópicos cadastrados nos eventos:")
   print(Events.get_topics())


if __name__ == "__main__":
   asyncio.run(main())
