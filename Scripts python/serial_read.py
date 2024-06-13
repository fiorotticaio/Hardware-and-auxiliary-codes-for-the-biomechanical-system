import serial
import csv

# Serial Port Settings
serial_port = serial.Serial('COM9', baudrate=9600)
file_name = 'test.csv' # flexion.csv or extension.csv

try:
    with open(file_name, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)  # Definindo o delimitador como ';'

        while True:
            data = serial_port.readline().decode('utf-8').strip() # Read data from serial port

            # Split the data string into a list of values
            values = data.split(',')[0:2] # Get the first two values

            print(values)

            # Writing to CSV file
            writer.writerow(values)

except KeyboardInterrupt:
    print("Stopped by user")

# Close the connection to the serial port
serial_port.close()