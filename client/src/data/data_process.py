import statistics
import matplotlib.pyplot as plt
import numpy as np
import random
import csv


DECIMAL_PLACES = 2
FILE_LOCATION = '../generated_files/'

client_data = list()
server_data = list()
server_mena_data = list()


def new_server(server):
    client_data.append({
        "server": server['name'],
        "data": list()
    })

    server_data.append({
        "server": server['name'],
        "data": list()
    })


def client_data_processing(size, payload):
    client_data[-1]['data'].append({
        "size": size,
        "time": float(round(statistics.mean(payload), 2))
    })


def server_data_processing(size, payload):
    """
    Combining the gathered server data into an object list.
    """

    server_data[-1]['data'].append({
        "size": size,
        "time": {
            "seq": float(round(statistics.mean(payload['seq']), DECIMAL_PLACES)),
            "sort": float(round(statistics.mean(payload['sort']), DECIMAL_PLACES))
        }
    })


def gather_data(type, size, payload):
    switcher = {
        "CLIENT": client_data_processing,
        "SERVER": server_data_processing
    }
    function = switcher.get(type)
    function(size, payload)


def server_type_average(server_data):
    """
    Takes the gathered server data and takes the average value of the two different types.
    """

    server_avg_data = list()

    for data_block in server_data:
        comb_seq_data = list()
        comb_sort_data = list()

        for data_set in data_block['data']:
            comb_seq_data.append(data_set['time']['seq'])
            comb_sort_data.append(data_set['time']['sort'])

        avg_sort_percentage = float(round(statistics.mean(comb_seq_data), DECIMAL_PLACES)) / float(
            round(statistics.mean(comb_sort_data), DECIMAL_PLACES))

        avg_seq_percentage = 100 - avg_sort_percentage

        server_avg_data.append({
            "server": data_block['server'],
            "data": {
                "seq": avg_seq_percentage,
                "sort": avg_sort_percentage
            }
        })

    return server_avg_data


def plot_client():
    plt.close()
    colors = ['#2d7f5e', '#78909C', '#FF7043', '#D32F2F', '#1E88E5', '#8E24AA']

    plt.title('Client RTT for OPC-UA load test')
    plt.ylabel('Client RTT (ms)')
    plt.xlabel('Data size')
    plt.grid(True)

    x_labels = list()

    for data_block in client_data:
        x_values = list()
        y_values = list()

        color_value = random.choice(colors)
        colors.remove(color_value)

        for data_set in data_block['data']:
            x_values.append(data_set['size'])
            y_values.append(float(data_set['time']))

        plt.plot(x_values, y_values, linestyle='-', marker='o',
                 color=color_value, linewidth=2, label=data_block['server'])

    plt.xticks(rotation=-45)
    plt.margins(0.5)
    plt.subplots_adjust(bottom=0.2)
    plt.legend()
    plt.savefig(FILE_LOCATION + 'client_plot.png')


def plot_server(server_data):
    plt.close()

    barWidth = 1
    plot_data = {
        "systems": list(),
        "seq": list(),
        "sort": list()
    }
    plt.title('Server RTT devided by action')
    plt.ylabel('RTT (%)')
    plt.xlabel('Systems')

    for data_block in server_data:
        plot_data['systems'].append(data_block['server'])
        plot_data['seq'].append(float(data_block['data']['seq']))
        plot_data['sort'].append(float(data_block['data']['sort']))

    plt.xticks(np.arange(len(plot_data)),
               plot_data['systems'])

    # Create bottom bars
    plt.bar(np.arange(len(plot_data)), plot_data['seq'], color='#FF5252', edgecolor='#424242',
            width=barWidth, label='Number generation')

    # Create top bar on top of the bottom one
    plt.bar(np.arange(len(plot_data)), plot_data['sort'], bottom=plot_data['seq'], color='#536DFE',
            edgecolor='#424242', width=barWidth, label='Sort operation')

    plt.legend()
    plt.savefig(FILE_LOCATION + 'server_plot.png')


def server_table():
    """
    Extract data from the server data set and devide it into n csv files.
    The files has the server name given in server list.
    """

    for data_block in server_data:
        with open(FILE_LOCATION + data_block['server'] + '_result.csv', 'w') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=',')
            file_writer.writerow(["Data size", "List generation", "List sort"])

            for data_set in data_block['data']:
                file_writer.writerow([
                    data_set['size'],
                    str(data_set['time']['seq']) + " ms",
                    str(data_set['time']['sort']) + " ms"
                ])


def compile_result():
    plot_server(server_type_average(server_data))
    plot_client()
    server_table()
