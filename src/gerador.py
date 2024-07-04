import time
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

class Gerador(Agent):
    grau = random.randint(1,3) #escolhe grau aleatório para a função
    a= random.randint(-100,100)
    raizes =[0,0,0]
    aux = [0,0,0]
    for i in range(grau):
        raizes[i] = random.randint(-1000,1000)
        aux[i] = 1

    function_type ={
            '1':f'{a}*(x-({raizes[0]}))',
            '2':f'{a}*(x-({raizes[0]}))*(x-({raizes[1]}))',
            '3':f'{a}*(x-({raizes[0]}))*(x-({raizes[1]}))*(x-({raizes[2]}))'
    }
        
    class funcao(CyclicBehaviour):
        #alterar forma de gerar funcao, senao so vai gerar grau 3
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                dom = eval(res.body)
                valores = []
                
                function ={
                    '1':[float(Gerador.a*(Gerador.aux[0]*x-Gerador.raizes[0])) for x in dom],
                    '2':[float(Gerador.a*(Gerador.aux[0]*x-Gerador.raizes[0])*(Gerador.aux[1]*x-Gerador.raizes[1])) for x in dom],
                    '3':[float(Gerador.a*(Gerador.aux[0]*x-Gerador.raizes[0])*(Gerador.aux[1]*x-Gerador.raizes[1])*(Gerador.aux[2]*x-Gerador.raizes[2])) for x in dom]
                }

                valores = function[str(Gerador.grau)]
                msg = Message(to=str(res.sender))
                msg.set_metadata('performative', 'inform')
                msg.body = str(valores)
                await self.send(msg)

    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                
                graus = {
                    '1':'grau1',
                    '2':'grau2',
                    '3':'grau3',
                }

                msg.body = graus[str(Gerador.grau)]
                await self.send(msg)
                # print("Respondeu para" + str(msg.sender) + " com " + msg.body)
            else:
                self.kill()
                
    async def setup(self):
        t = Template()
        t.set_metadata("performative","subscribe")
        tf = self.funcao()
        
        self.add_behaviour(tf,t)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)

        print(f'Função gerada: {Gerador.function_type[str(Gerador.grau)]}')

async def main():

    gerador = Gerador("geradorlufel@jix.im", "Gerador123!")
    await gerador.start()
    print('gerador iniciado')

    while gerador.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            gerador.stop()
            break
    print("Agente encerrou!")

if __name__ == '__main__':
    spade.run(main())