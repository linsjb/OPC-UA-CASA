import logging
import asyncio
from random import randint

from asyncua import ua, Server
from asyncua.common.methods import uamethod


async def main():
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://opc-server:4880')

    namespace = await server.register_namespace("OPC-UA-CASA")
    rootnode = server.get_objects_node()

    param = await rootnode.add_object(namespace, "rootObject")
    value = await param.add_variable(namespace, "randVariable", 0)
    await value.set_writable()

    async with server:
        while True:
            randValue = randint(10, 20)
            print(randValue)
            await value.set_value(randValue)
            await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
