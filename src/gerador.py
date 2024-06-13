import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

class Gerador(Agent):
    grau = random.randint(1,3) #escolhe grau aleatório para a função
    a=0
    while a == 0:
        a = random.randint(-100,100)
    if grau==1:
        x1 = random.randint(-1000,1000)
        y = -1 * (a*x1)
    elif grau==2:
        x1 = random.randint(-1000,1000)
        x2 = random.randint(-1000,1000)
    else:
        x1 = random.randint(-1000,1000)
        x2 = random.randint(-1000,1000)
        x3 = random.randint(-1000,1000)
        
        
    class funcao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = eval(res.body)
                valores = []
                if Gerador.grau == 1:
                    valores = [float(Gerador.a*x + Gerador.y) for x in [0,1,2,3,4]]
                elif Gerador.grau == 2:
                    valores = [float(Gerador.a*(x-Gerador.x1)*(x-Gerador.x2)) for x in [0,1,2,3,4]]
                else:
                    valores = [float(Gerador.a*(x-Gerador.x1)*(x-Gerador.x2)*(x-Gerador.x3)) for x in [0,1,2,3,4]]
                
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "request")  
                msg.body = str(valores)
                await self.send(msg)

    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                if Gerador.grau==1:
                    msg.body = "1grau" 
                elif Gerador.grau==2:
                    msg.body = "2grau"
                else:
                    msg.body = "3grau"
                await self.send(msg)
                # print("Respondeu para" + str(msg.sender) + " com " + msg.body)
            else:
                self.kill()
                
    async def setup(self):
        t = Template()
        t.set_metadata("performative","inform")
        tf = self.funcao()
        
        self.add_behaviour(tf,t)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)

        if Gerador.grau==1:
            print("Funcao de 1o grau: ")
            print(Gerador.a, "x + (", Gerador.y, ")")
        elif Gerador.grau==2:
            print("Funcao de 2o grau: ")
            print(f'{Gerador.a}*(x-({Gerador.x1}))*(x-({Gerador.x2}))')
        else:
            print("Funcao de 3o grau: ")
            print(f'{Gerador.a}*(x-({Gerador.x1}))*(x-({Gerador.x2}))*(x-({Gerador.x3}))')