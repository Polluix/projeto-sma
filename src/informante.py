import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import numpy as np

class Informante(Agent):
    valores_y = []
    class get_values(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "subscribe")
            
                message = Message(to="geradorlufel@jix.im")
                message.set_metadata("performative", "inform")
                message.body='[0,1,2,3,4]'

                await self.send(message)
                valor = await self.receive(timeout=5)
                if valor:
                    msg.body = valor.body

                    await self.send(msg)

    async def setup(self):
        t = Template()
        t.set_metadata("performative", "request")

        b = self.get_values()
        self.add_behaviour(b,t)