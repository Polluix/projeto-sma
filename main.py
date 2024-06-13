import spade
from src.resolvedor import Resolvedor
from src.gerador import Gerador
from src.informante import Informante
from spade import wait_until_finished

async def main():

    gerador = Gerador("geradorlufel@jix.im", "Gerador123!")
    await gerador.start()
    print('gerador iniciado')

    
    informante = Informante("obtentorlufel@jix.im", "Informante123!")
    await informante.start()
    print('informante iniciado')
    
    resolvedor = Resolvedor('resolvedorlufel@jix.im', 'Resolvedor123!')
    await resolvedor.start()
    print('resolvedor iniciado')
    
    

    

if __name__=='__main__':
    spade.run(main())
