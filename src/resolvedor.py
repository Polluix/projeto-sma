import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour,OneShotBehaviour
from spade.message import Message
from spade.template import Template
import time
import numpy as np

GRAU_MAX = 3

class Resolvedor(Agent):
    valores_y = []
    valores_x = []
    grau = 0

    class get_values(CyclicBehaviour):
        async def run(self):
            if len(Resolvedor.valores_y) < Resolvedor.grau+1:
                msg = Message(to="geradorlufel@jix.im")
                msg.set_metadata("performative", "subscribe")
                
                x = np.random.randint(-1000,1000)
                msg.body=str(x)

                if x not in Resolvedor.valores_x:
                    await self.send(msg)
                    Resolvedor.valores_x.append(x)

                    valor = await self.receive(timeout=5)
                    
                    if valor:
                        Resolvedor.valores_y.append(eval(valor.body))
                    
            else:
                time.sleep(5) #nao resolve a equação se nao houver essa pausa
                self.agent.add_behaviour(Resolvedor.solve_equation())
                self.kill()

    class get_grau(OneShotBehaviour):
        async def run(self):
            if Resolvedor.grau==0:
                msg = Message(to="geradorlufel@jix.im")
                msg.set_metadata('performative', 'request')
                await self.send(msg)
                grau_recebido = await self.receive(timeout=5)
                if grau_recebido:
                    Resolvedor.grau = int(grau_recebido.body.split('grau')[0])
                    self.agent.add_behaviour(Resolvedor.get_values())
                
    class solve_grau1(OneShotBehaviour):
        async def run(self):
            x1 = 0

            msg = Message(to='geradorlufel@jix.im')
            msg.set_metadata('performative', 'subscribe')
            msg.body='0'
            await self.send(msg)

            img_0 = await self.receive(timeout=5)
            y1 = eval(img_0.body)

            x2 = Resolvedor.valores_x[1]
            y2 = Resolvedor.valores_y[1]

            a = (y2-y1)/(x2-x1)
            
            b = y1
            print(f'Raíz da função do 1o grau: {-b/a}\n')

    class solve_grau2(OneShotBehaviour):
        async def run(self):
            #sistema para resolução numérica
            mat = np.zeros((Resolvedor.grau+1,Resolvedor.grau+1))
            mat[:,-1]=1
            mat[:,0] = [Resolvedor.valores_x[0]**2,Resolvedor.valores_x[1]**2,Resolvedor.valores_x[2]**2]
            mat[:,1] = [Resolvedor.valores_x[0],Resolvedor.valores_x[1],Resolvedor.valores_x[2]]

            coeficientes = np.linalg.solve(mat,Resolvedor.valores_y[:])

            raizes = np.roots(coeficientes)
            raizes = [round(i) for i in raizes]

            print(f'Solução da equação do {Resolvedor.grau}o grau: {raizes}')

    class solve_grau3(OneShotBehaviour):
        async def run(self):
            #sistema para resolução numérica
            mat = np.zeros((Resolvedor.grau+1,Resolvedor.grau+1))
            
            mat[:,-1]=1
            mat[:,0] = [Resolvedor.valores_x[0]**3,Resolvedor.valores_x[1]**3,Resolvedor.valores_x[2]**3,Resolvedor.valores_x[3]**3]
            mat[:,1] = [Resolvedor.valores_x[0]**2,Resolvedor.valores_x[1]**2,Resolvedor.valores_x[2]**2,Resolvedor.valores_x[3]**2]
            mat[:,2] = [Resolvedor.valores_x[0],Resolvedor.valores_x[1],Resolvedor.valores_x[2],Resolvedor.valores_x[3]]

            coeficientes = np.linalg.solve(mat,Resolvedor.valores_y[:])

            raizes = np.roots(coeficientes)
            raizes = [round(i) for i in raizes]

            print(f'Solução da equação do {Resolvedor.grau}o grau: {raizes}')

                
    class solve_equation(OneShotBehaviour):
        async def run(self):
            if Resolvedor.grau!=0:
                solvers = {
                    '1':Resolvedor.solve_grau1(),
                    '2':Resolvedor.solve_grau2(),
                    '3':Resolvedor.solve_grau3(),
                }
                solver = solvers[str(Resolvedor.grau)]
                self.agent.add_behaviour(solver)
                
    
    async def setup(self):
        # template_grau = Template()
        # template_grau.set_metadata('performative','inform')
        b1 = self.get_grau()
        self.add_behaviour(b1)



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