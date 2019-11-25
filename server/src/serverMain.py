import asyncio
from asyncua import ua, Server, uamethod
import datetime


@uamethod
def dataCall(parent, data):
    timeStart = datetime.datetime.now()
    dataProcess(data)
    timeEnd = datetime.datetime.now()
    timeDelta = timeEnd - timeStart
    print("Time delta:", timeDelta)
    return timeDelta.microseconds


def dataProcess(data):
    process = pow(2, data)
    print("Calculation result:", process)


async def initServer(endpoint, nsp):
    server = Server()
    await server.init()
    server.set_endpoint(endpoint)

    namespace = await server.register_namespace(nsp)
    rootNode = server.get_objects_node()
    obj = await rootNode.add_object(namespace, "BaseObjects")

    dataCallNode = await obj.add_method(
        namespace,
        "dataCall",
        dataCall,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64]

    )

    # multiply_node = await obj.add_method(
    #     namespace,
    #     "multiply",
    #     multiply,
    #     [ua.VariantType.Int64, ua.VariantType.Int64],
    #     [ua.VariantType.Int64]
    # )

    await server.start()

    try:
        print("OPC-UA server started")
        while True:
            await asyncio.sleep(1)
    finally:
        await server.stop()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initServer(
        'opc.tcp://opc-server:4881', 'OPC-UA-CASA'))
    loop.close()


if __name__ == '__main__':
    main()
