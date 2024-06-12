import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
import random

class Resolvedor(Agent):
    class send_x(CyclicBehaviour):
        x = -1000

        async def run(self):
            message = Message(to="geradorlufel@jix.im")
            message.set_metadata("performative", "inform")
            message.body=str(self.x)

            await self.send(message)
            msg = await self.receive(timeout=1)
            
            if msg.body=='0':
                print(f'Raíz encontrada: {self.x}\nFinalizando Resolvedor...\n')
                self.kill()
            else:
                self.x +=1

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        b = self.send_x()
        self.add_behaviour(b)