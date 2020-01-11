import asyncio
from asyncua import ua, Server, uamethod
import datetime
import random
import time
import yaml


class Server_tests:
    def __init__(self, server_rtt, data_pool):
        self.server_rtt = server_rtt
        self.data_pool = data_pool

    @uamethod
    async def random_sort(self, parent, data_size, data_range):
        temp_data_pool = list()

        start_sequence_time = time.time()

        for _ in range(data_size):
            temp_data_pool.append(random.randint(1, data_range))

        end_sequence_time = time.time()

        start_sort_time = time.time()
        temp_data_pool.sort()
        end_sort_time = time.time()

        await self.data_pool.set_value(temp_data_pool)

        sequence_delta = (end_sequence_time - start_sequence_time) * 1000
        sort_delta = (end_sort_time - start_sort_time) * 1000

        server_rtt_fragments = list()
        server_rtt_fragments.append(sequence_delta)
        server_rtt_fragments.append(sort_delta)
        await self.server_rtt.set_value(server_rtt_fragments)

        print(f'Seq time: {sequence_delta}, Sort time: {sort_delta}')


async def init_server():
    with open(r'../configuration.yml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

        server = Server()
        await server.init()
        server.set_endpoint(
            "opc.tcp://" + config['host'] + ":" + str(config['port']))

        namespace = await server.register_namespace(config['namespace'])
        root_node = server.get_objects_node()
        objects = await root_node.add_object(namespace, "BaseObjects")

        server_rtt = await objects.add_variable(
            namespace,
            "server_rtt",
            None
        )

        data_pool = await objects.add_variable(
            namespace,
            "data_pool",
            None
        )

        await server_rtt.set_writable()
        await data_pool.set_writable()

        server_tests = Server_tests(server_rtt, data_pool)

        server.link_method(root_node, server_tests.random_sort)

        random_sort_method = await objects.add_method(
            namespace,
            "random_sort",
            server_tests.random_sort,
            [ua.VariantType.Int64, ua.VariantType.Int64],
            [ua.VariantType.Int64]
        )

        await server.start()

        try:
            print("OPC-UA server started")
            # while True:
            #     await asyncio.sleep(1)
        finally:
            await server.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_server())
    loop.close()
