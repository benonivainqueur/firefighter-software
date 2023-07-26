import asyncio
import logging
import pathlib

from websockets import serve

data_location = pathlib.Path(__file__).parent.resolve() / "heart_data"  # change per setup ?
input_filename = data_location / (input("Name log file: ") + '.log')
logging.basicConfig(filename=input_filename, filemode='a+', format='%(created)f|%(message)s', level=logging.INFO)
logger = logging.getLogger('main')
CURRENT_ACTION = False


async def echo(websocket):
    async for message in websocket:
        print(message)
        global CURRENT_ACTION
        if message == 'START':
            CURRENT_ACTION = True
        elif message == 'STOP':
            CURRENT_ACTION = False

        if 'a+' in message:
            if CURRENT_ACTION:
                logger.info(message)
        else:
            logger.info(message)
        # await websocket.send(message)


async def main():
    async with serve(echo, "0.0.0.0", 8008):
        await asyncio.Future()


asyncio.run(main())
