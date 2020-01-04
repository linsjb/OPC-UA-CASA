import asyncio
import datetime
from asyncua import Client, Node
import sys
import enum
import time
import statistics
from data import data_process


async def serverMethodCall(args):
    for data_size in args['data_sizes']:
        for data_range in args['data_ranges']:
            print(
                f'\nServer: {args["server"]["server"]}, Data size: {data_size}, Data range: {data_range}, Client iterations: {args["client_iterations"]}')
            print('--------------')

            data = {}
            client_rtt_data = list()
            server_rtt_data = {}
            server_rtt_seq_data = list()
            server_rtt_sort_data = list()

            current_data_size = str(data_size) + "," + str(data_range)

            for i in range(args['client_iterations']):
                time_start = time.time()

                await args['objects'].call_method(
                    "2:random_sort",
                    data_size,
                    data_range
                )

                remote_data_pool = await args['data_pool'].get_value()
                remote_server_rtt = await args['server_rtt'].get_value()

                time_end = time.time()

                client_rtt = (time_end - time_start)*1000

                client_rtt_data.append(client_rtt)
                server_rtt_seq_data.append(remote_server_rtt[0])
                server_rtt_sort_data.append(remote_server_rtt[1])

                print(f'Client RTT on iteration {i+1} = {client_rtt} ms')

            data_process.gather_data(
                "CLIENT_MEAN", current_data_size, client_rtt_data)

            server_rtt_data['seq'] = server_rtt_seq_data
            server_rtt_data['sort'] = server_rtt_sort_data

            data_process.gather_data(
                'SERVER_MEAN', current_data_size, server_rtt_data)

            data_process.server(args['server']['server'])


async def init_server():

    servers = [{
        "server": 'opc-server:4881',
        "name": "Reference system"
    }, {
        "server": 'opc-server:4881',
        "name": "RPi 1"
    }]

    for server in servers:
        async with Client(url='opc.tcp://' + server['server']) as client:
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

            data_sizes = [
                10000
            ]

            data_ranges = [
                100
            ]

            args = {
                'objects': objects,
                'server_rtt': server_rtt,
                'data_pool': data_pool,
                'client_iterations': int(sys.argv[1]),
                'data_ranges': data_ranges,
                'data_sizes': data_sizes,
                'server': server
            }

            await serverMethodCall(args)
            data_process.print_result()
            # data_process.plot_client()
            # data_process.plot_server()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_server())
    loop.close()
