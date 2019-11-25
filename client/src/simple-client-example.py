import asyncio
import sys
sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua
import time

async def main():
    async with Client(url='opc.tcp://localhost:4880') as client:
        root = client.get_root_node()

        namespace = await client.get_namespace_index("OPCUA_TEST_SERVER")
        variable = await root.get_child(["0:Objects", f"{namespace}:objektet", f"{namespace}:variabeln"])

        while True:
            print(await variable.get_value())
            time.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()