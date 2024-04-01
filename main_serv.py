
'''
сервер
'''
import asyncio
import logging
import websockets
from websockets import (
    WebSocketServerProtocol,
    serve,
    WebSocketProtocolError
)
import names
from websockets.exceptions import ConnectionClosedOK

from req import main_req

logging.basicConfig(level=logging.INFO)



class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        except WebSocketProtocolError as err:
            logging.error(err)
        finally:
            await self.unregister(ws)



    async def distrubute(self, ws: WebSocketServerProtocol):

        async for message in ws:
            if message=="курс":
                await self.send_to_clients(f"{ws.name}:{curse}")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 7070):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    curse=main_req()
    asyncio.run(main())
