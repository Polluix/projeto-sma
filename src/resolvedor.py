import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import time
import numpy as np

GRAU_MAX = 3

class Resolvedor(Agent):
    valores_y = []
    valores_x = [0,1,2,3,4]
    grau = 0

    class get_values(CyclicBehaviour):
        async def run(self):
            msg = Message(to="geradorlufel@jix.im")
            msg.set_metadata("performative", "inform")
            msg.body='[0,1,2,3,4]'
            await self.send(msg)
            valor = await self.receive(timeout=5)
            if valor:
                Resolvedor.valores_y = eval(valor.body)

    class get_grau(CyclicBehaviour):
        async def run(self):
            if len(Resolvedor.valores_y)!=0:
                diferencas = np.diff(Resolvedor.valores_y)
                for i in range(GRAU_MAX):
                    if np.all(diferencas==diferencas[0]):
                        Resolvedor.grau = i+1 #retorna grau da função
                        break
                    else:
                        diferencas = np.diff(diferencas)

    class solve_grau1(CyclicBehaviour):
        async def run(self):
            x1 = Resolvedor.valores_x[0]
            x2 = Resolvedor.valores_x[1]
            y1 = Resolvedor.valores_y[0]
            y2 = Resolvedor.valores_y[1]

            a = (y2-y1)/(x2-x1)
            b = y1
            print(f'Raíz da função do 1o grau: {-b/a}\n')
            self.kill()

    class solve_grau2(CyclicBehaviour):
        async def run(self):
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

    class solve_grau3(CyclicBehaviour):
        async def run(self):
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

                
    class solve_equation(CyclicBehaviour):
        async def run(self):
            if Resolvedor.grau!=0:
                solvers = {
                    '1':Resolvedor.solve_grau1(),
                    '2':Resolvedor.solve_grau2(),
                    '3':Resolvedor.solve_grau3(),
                }
                solver = solvers[str(Resolvedor.grau)]

                self.agent.add_behaviour(solver)
                self.kill()
                
    
    async def setup(self):

        t2 = Template()
        t2.set_metadata('performative', 'request')
        valores = self.get_values()
        self.add_behaviour(valores,t2)

        t1 = Template()
        t1.set_metadata('performative', 'subscribe')

        b1 = self.get_grau()
        self.add_behaviour(b1,t1)

        behaviour = self.solve_equation()
        self.add_behaviour(behaviour)

async def main():
    resolvedor = Resolvedor('resolvedorlufel@jix.im', 'Resolvedor123!')
    await resolvedor.start()
    print('resolvedor iniciado')

    while resolvedor.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            resolvedor.stop()
            break
    print("Agente encerrou!")

if __name__=='__main__':
    spade.run(main())