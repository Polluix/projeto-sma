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
    for i in range(grau):
        raizes[i] = random.randint(-1000,1000)

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
                x = eval(res.body)
                
                function ={
                    '1':float(Gerador.a*(x-Gerador.raizes[0])),
                    '2':float(Gerador.a*(x-Gerador.raizes[0])*(x-Gerador.raizes[1])),
                    '3':float(Gerador.a*(x-Gerador.raizes[0])*(x-Gerador.raizes[1])*(x-Gerador.raizes[2]))
                }

                valor = function[str(Gerador.grau)]

                msg = Message(to=str(res.sender))
                msg.set_metadata('performative', 'inform')
                msg.body = str(valor)
                await self.send(msg)
                # print("Respondeu para " + str(msg.sender))

    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                
                graus = {
                    '1':'1grau',
                    '2':'2grau',
                    '3':'3grau',
                }

                msg.body = graus[str(Gerador.grau)]
                await self.send(msg)
                # print("Respondeu para" + str(msg.sender) + " com " + msg.body)
                
    async def setup(self):
        t = Template()
        t.set_metadata("performative", "subscribe")
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