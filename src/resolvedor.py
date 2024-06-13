import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import numpy as np

GRAU_MAX = 3

class Resolvedor(Agent):
    valores_y = []
    valores_x = [0,1,2,3,4]
    grau = 0
    class imagem(CyclicBehaviour):
        async def run(self):
            for i in range(5):
                message = Message(to="obtentorlufel@jix.im")
                message.set_metadata("performative", "request")
                await self.send(message)
                valor = await self.receive(timeout=5)
                if valor:
                    Resolvedor.valores_y = eval(valor.body)

    class get_grau(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                diferencas = np.diff(Resolvedor.valores_y)
                for i in range(GRAU_MAX):
                    if np.all(diferencas==diferencas[0]):
                        Resolvedor.grau = i+1 #retorna grau da função
                        break
                    else:
                        diferencas = np.diff(diferencas)
                
    class solve_equation(CyclicBehaviour):
        async def run(self):
            if Resolvedor.valores_y != []:
                if Resolvedor.grau==1:
                    x1 = Resolvedor.valores_x[0]
                    x2 = Resolvedor.valores_x[1]
                    y1 = Resolvedor.valores_y[0]
                    y2 = Resolvedor.valores_y[1]

                    a = (y2-y1)/(x2-x1)
                    b = y1
                    
                    print(f'Raíz da função do 1o grau: {-b/a}\n')
                    self.kill()
                    
                elif Resolvedor.grau==2:
                    #montar sistema para resolver numericamente para grau 2 e 3
                    mat = np.zeros((Resolvedor.grau+1,Resolvedor.grau+1))

                    mat[:,-1]=1
                    mat[:,0] = [Resolvedor.valores_x[1]**2,Resolvedor.valores_x[2]**2,Resolvedor.valores_x[3]**2]
                    mat[:,1] = [Resolvedor.valores_x[1],Resolvedor.valores_x[2],Resolvedor.valores_x[3]]

                    coeficientes = np.linalg.solve(mat,Resolvedor.valores_y[1:4])

                    raizes = np.roots(coeficientes)
                    raizes = [round(i) for i in raizes]

                    print(f'Solução da equação do {Resolvedor.grau}o grau: {raizes}')
                    self.kill()
                else:
                    #montar sistema para resolver numericamente para grau 2 e 3

                    mat = np.zeros((Resolvedor.grau+1,Resolvedor.grau+1))
                    
                    mat[:,-1]=1
                    mat[:,0] = [Resolvedor.valores_x[1]**3,Resolvedor.valores_x[2]**3,Resolvedor.valores_x[3]**3,Resolvedor.valores_x[4]**3]
                    mat[:,1] = [Resolvedor.valores_x[1]**2,Resolvedor.valores_x[2]**2,Resolvedor.valores_x[3]**2,Resolvedor.valores_x[4]**2]
                    mat[:,2] = [Resolvedor.valores_x[1],Resolvedor.valores_x[2],Resolvedor.valores_x[3],Resolvedor.valores_x[4]]

                    coeficientes = np.linalg.solve(mat,Resolvedor.valores_y[1:])

                    raizes = np.roots(coeficientes)
                    raizes = [round(i) for i in raizes]

                    print(f'Solução da equação do {Resolvedor.grau}o grau: {raizes}')
                    self.kill()
    
    async def setup(self):
        t = Template()
        t.set_metadata('performative', 'subscribe')

        b = self.imagem()
        self.add_behaviour(b,t)

        t1 = Template()
        t1.set_metadata('performative', 'subscribe')

        b1 = self.get_grau()
        self.add_behaviour(b1,t1)

        behaviour = self.solve_equation()
        self.add_behaviour(behaviour)