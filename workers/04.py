import asyncio

"""
O Problema: Um Producer coloca 10 números em uma asyncio.Queue. Um Consumer retira esses números para processar.

1.  O Consumer deve ter um timeout de 2 segundos para cada item.
2.  Simule que, se o número for "7", o processamento demora 5 segundos (causando um estouro de timeout).
3.  Seu código deve capturar a exceção de timeout, avisar que o "Item 7 falhou" e continuar processando o restante da fila sem travar o programa.
"""

async def main():
    await asyncio.sleep(1)

if __name__ == "__main__":
    print("Hello, world")