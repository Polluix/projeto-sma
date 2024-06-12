import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
import random

class Resolvedor(Agent):

    class send_x(OneShotBehaviour):
        async def run(self):
            x = random.randint(-1000,1000)
            message = Message(to="geradorlufel@jix.im")
            message.set_metadata("performative", "inform")
            message.body=str(x)

            await self.send(message)
            await self.agent.stop()
            

    async def setup(self):
        b = self.send_x()
        self.add_behaviour(b)