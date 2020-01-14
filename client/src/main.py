import asyncio
import datetime
from asyncua import Client, Node
import sys
import enum
import time
import statistics
from data import data_process
import yaml


async def server_method_call(args):
    for data_size in args['data_sizes']:
        print(
            f'\n\nServer: {args["server"]["ip"]} ({args["server"]["name"]}), Data size: {data_size}, Client iterations: {args["client_iterations"]}'
        )
        print('--------------')

        client_rtt_data = list()
        server_rtt_seq_data = list()
        server_rtt_sort_data = list()

        for i in range(args['client_iterations']):
            time_start = time.time()

            await args['objects'].call_method(
                "2:random_sort",
                data_size,
                args['data_range']['min'],
                args['data_range']['max']
            )

            remote_data_pool = await args['data_pool'].get_value()
            remote_server_rtt = await args['server_rtt'].get_value()

            time_end = time.time()

            client_rtt = (time_end - time_start)*1000

            client_rtt_data.append(client_rtt)

            server_rtt_seq_data.append(remote_server_rtt[0])
            server_rtt_sort_data.append(remote_server_rtt[1])

            print(
                f'Client RTT on iteration {i+1} = {str(round(client_rtt, 2))} ms'
            )

        print(
            f'Average value: {str(round(statistics.mean(client_rtt_data), 2))} ms'
        )

        data_process.gather_data(
            "CLIENT", data_size, client_rtt_data)

        data_process.gather_data('SERVER', data_size, {
            "seq": server_rtt_seq_data,
            "sort": server_rtt_sort_data
        })


async def init_server():
    with open(r'../configuration.yml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    for server in config['servers']:
        data_process.new_server(server)
        async with Client(url='opc.tcp://' + str(server['ip']) + ':' + str(server['port'])) as client:
            root_object = "0:Objects"
            root_node = client.get_root_node()
            namespace = await client.get_namespace_index("OPC-UA-CASA")

            objects = await root_node.get_child([
                root_object,
                f"{namespace}:BaseObjects"
            ])

            server_rtt = await root_node.get_child([
                root_object,
                f"{namespace}:BaseObjects",
                f"{namespace}:server_rtt"
            ])

            data_pool = await root_node.get_child([
                root_object,
                f"{namespace}:BaseObjects",
                f"{namespace}:data_pool"
            ])

            args = {
                'objects': objects,
                'server_rtt': server_rtt,
                'data_pool': data_pool,
                'client_iterations': int(sys.argv[1]),
                'data_sizes': config['data_sizes'],
                'data_range': {
                    'min': config['data_range']['min'],
                    'max': config['data_range']['max']
                },
                'server': server
            }

            await server_method_call(args)

    data_process.compile_result(config['graph_filetypes'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_server())
    loop.close()
