import spade
from src.resolvedor import Resolvedor
from src.gerador import Gerador
from spade import wait_until_finished

async def main():
    gerador = Gerador("geradorlufel@jix.im", "Gerador123!")
    # resolvedor = Resolvedor("resolvedorlufel@jix.im", "Resolvedor123!")
    
    await gerador.start()
    print("DummyAgent started. Check its console to see the output.")

    print("Wait until user interrupts with ctrl+C")
    await wait_until_finished(gerador)
    print('gerador terminado')

    # await resolvedor.start()
    # print("DummyAgent started. Check its console to see the output.")

    # print("Wait until user interrupts with ctrl+C")
    # await wait_until_finished(resolvedor)
    # print('resolvedor terminado')

if __name__=='__main__':
    spade.run(main())
