import statistics
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc


client_data = {}
server_seq_mean = {}
server_sort_mean = {}

server_data = {
    "seq": server_seq_mean,
    "sort": server_sort_mean
}

gathered_data = {
    "client": client_data,
    "server": server_data
}

data = {}


def client_mean(size, payload):
    current_client_rtt_mean = list()
    current_client_rtt_mean = statistics.mean(payload)
    client_data[size] = current_client_rtt_mean


def server_mean(size, payload):
    current_server_seq_mean = list()
    current_server_sort_mean = list()
    current_server_seq_mean = statistics.mean(payload['seq'])
    current_server_sort_mean = statistics.mean(payload['sort'])

    server_seq_mean[size] = current_server_seq_mean
    server_sort_mean[size] = current_server_sort_mean


def server(name):
    data[name] = gathered_data


def gather_data(type, size, payload):
    switcher = {
        "CLIENT_MEAN": client_mean,
        "SERVER_MEAN": server_mean
    }
    function = switcher.get(type)
    function(size, payload)


def print_result():
    print(data)


def plot_client():
    plt.close()
    # evenly sampled time at 200ms intervals

    t = np.arange(0., 5., 0.2)

    # red dashes, blue squares and green triangles

    plt.title('Client RTT for OPC-UA load test')
    plt.ylabel('Client RTT (ms)')
    plt.xlabel('Data size')

    plt.plot(t, t**2.4, 'r', label='RpI 1')
    plt.plot(t, t**2, 'g', label='RpI 3')
    plt.plot(t, t**1.2, 'b', label='Ref. system')

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
