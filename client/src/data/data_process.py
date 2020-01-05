import statistics
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
import random

DECIMAL_PLACES = 2

client_data = list()
server_data = list()


def new_server(server):
    client_data.append({
        "server": server['name'],
        "data": list()
    })

    server_data.append({
        "server": server['name'],
        "data": list()
    })


def client_mean(server, size, payload):
    data_point = {}

    data_point['size'] = size
    data_point['time'] = str(round(statistics.mean(payload), 2))

    client_data[-1]['data'].append(data_point)


def server_mean(server, size, payload):
    server_time_types = {
        "seq": str(round(statistics.mean(payload['seq']), DECIMAL_PLACES)),
        "sort": str(round(statistics.mean(payload['sort']), DECIMAL_PLACES))
    }

    data_point = {}
    data_point['size'] = size
    data_point['time'] = server_time_types

    server_data[-1]['data'].append(data_point)


def gather_data(type, server, size, payload):
    switcher = {
        "CLIENT_MEAN": client_mean,
        "SERVER_MEAN": server_mean
    }
    function = switcher.get(type)
    function(server, size, payload)


def print_result():
    print('\n\n=== Results ===')
    print(f'Client data: {client_data}')
    print(f'Server data: {server_data}')


def test():
    for data in client_data:
        for sett in data['data']:
            print(sett['size'])


def plot_client():
    plt.close()
    colors = ['r', 'g', 'b']

    plt.title('Client RTT for OPC-UA load test')
    plt.ylabel('Client RTT (ms)')
    plt.xlabel('Data size')
    plt.grid(True)

    for data_block in client_data:
        x_values = list()
        y_values = list()
        for data_set in data_block['data']:
            x_values.append(data_set['size'])
            y_values.append(float(data_set['time']))
        color = random.choice(colors)
        plt.plot(x_values, y_values, linestyle='-',
                 marker='o', color=color, label=data_block['server'])

    # plt.plot(x, y, 'bo', label='AAA',)
    # plt.plot(t, t**2, 'b', label='BBB')
    # plt.plot(t, t**1.2, 'b', label='Ref. system')

    plt.legend()
    plt.savefig('client_plot.png')


def plot_server():
    plt.close()
    # y-axis in bold
    rc('font', weight='bold')

    # Values of each group
    randomSeq = [40, 30, 10]
    sortSeq = [60, 50, 20]

    # The position of the bars on the x-axis
    r = [0, 1, 2]

    # Names of group and bar width
    names = ['RPi 1', 'RPi 3', 'Ref. system']
    barWidth = 1

    # Create brown bars
    plt.bar(r, randomSeq, color='#7f6d5f', edgecolor='white',
            width=barWidth, label='Random operation')
    # Create green bars (middle), on top of the firs ones
    plt.bar(r, sortSeq, bottom=randomSeq, color='#2d7f5e',
            edgecolor='white', width=barWidth, label='Sort operation')

    # Custom X axis
    plt.xticks(r, names, fontweight='bold')
    plt.title('Server RTT devided by action')
    plt.ylabel('RTT (ms)')

    # Show graphic
    plt.legend()
    plt.savefig('server_plot.png')
