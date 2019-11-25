import asyncio
import datetime
from asyncua import Client, Node


async def main():
    async with Client(url='opc.tcp://opc-server:4881') as client:
        nodes = client.get_root_node()
        opcNamespace = await client.get_namespace_index("OPC-UA-CASA")
        obj = await nodes.get_child(["0:Objects", "2:BaseObjects"])

        timeStart = datetime.datetime.now()
        serverTimeDelta = await obj.call_method("2:dataCall", 5000)
        timeEnd = datetime.datetime.now()

        clientRoundTripTime = timeEnd - timeStart
        print("Server time delta (microseconds):", serverTimeDelta)
        print("Client round trip time (microseconds):",
              clientRoundTripTime.microseconds)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
