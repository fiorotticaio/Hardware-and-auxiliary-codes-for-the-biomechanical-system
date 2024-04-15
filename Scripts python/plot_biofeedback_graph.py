import os
import matplotlib.pyplot as plt
import csv
import numpy as np

def plot_biofeedback_graph():
    directory_name = f'C:/Users/Caio/UFES/Engenharia da Computação/7º Período/PIC-II/Virtual-Reality-Controlled-by-Myoelectric-Signals/Data' # Absolute path

    # List all files in the directory_name that begin with 'biofeedback'
    files = [file for file in os.listdir(directory_name) if file.startswith('biofeedback')]
            
    # Function that slices de data to get the desired time interval
    def slice_data(data, initial_time, final_time):
        sliced_data = {}
        for key, value in data.items():
            if key >= initial_time and key <= final_time:
                sliced_data[key] = value
        return sliced_data

    i = 0
    # Iterates over the files and generates graphs for each one
    while i < len(files):
        file_path = os.path.join(directory_name, files[i]) # Full file path

        # Lists for storing current file data
        angles = []
        time = []

        # Separates data that is separated by a comma
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for line in csv_reader:
                n1, n2 = map(lambda x: float(x.replace(',', '.')), line)
                angles.append(n1)
                time.append(n2)

        data = dict(zip(time, angles)) # Making a dictionary with the data

        # Generates the graph for the current file
        plt.figure(figsize=(10, 8))
        plt.plot(data.keys(), data.values())
        plt.title(f'Virtual eblow angle - {files[i]}')
        plt.tight_layout()
        plt.show()

        # Getting the initial and final time to analyze
        initial_time = int(input('Initial time: '))
        final_time = int(input('Final time: '))
        base_angle = int(input('Base angle: '))

        data = slice_data(data, initial_time, final_time) # Slicing the lists to get the data in the desired time interval

        # Another slice after the first base_angle is reached
        for key, value in data.items():
            if value >= base_angle:
                data = slice_data(data, key, final_time)
                break

        # Get the minimum and maximum values of the data
        min_value = min(data.values())
        max_value = max(data.values())

        # Calculate the mean and standard deviation of the data
        mean = np.mean(list(data.values()))
        std = np.std(list(data.values()))

        # Plotting the zoom in graph
        plt.figure(figsize=(10, 8))
        plt.axhline(y=base_angle, color='g', linestyle='--', label=f'{base_angle}-degree line', linewidth=2)
        plt.axhline(y=min_value, color='purple', linestyle='--', label=f'min_value-degree line: {min_value:.2f}')
        plt.axhline(y=max_value, color='r', linestyle='--', label=f'max_value-degree line: {max_value:.2f}')
        plt.axhline(y=mean, color='black', linestyle='-', label=f'mean-degree line: {mean:.2f}')
        plt.axhline(y=mean + std, color='black', linestyle=':', label=f'mean + std-degree line: {mean + std:.2f}')
        plt.axhline(y=mean - std, color='black', linestyle=':', label=f'mean - std-degree line: {mean - std:.2f}')
        plt.plot(data.keys(), data.values())
        plt.title(f'Zoom in virtual prothesis angle- {files[i]}')
        plt.legend()
        plt.tight_layout()
        plt.show()


        # Ask if the user wants to repeat the same file
        repeat = input('Repeat the same file? (y/n): ')
        if repeat.lower() == 'n':
            i += 1