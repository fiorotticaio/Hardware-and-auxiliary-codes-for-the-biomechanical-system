import serial
import csv

# Serial Port Settings
porta_serial = serial.Serial('COM9', baudrate=9600)
file_name = 'flexion.csv' # flexion.csv or extension.csv

try:
    with open(file_name, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)  # Definindo o delimitador como ';'

        while True:
            data = porta_serial.readline().decode('utf-8').strip() # Read data from serial port

            print(data)
            
            # Split the data string into a list of values
            valores = data.split(',')
            
            # Writing to CSV file
            writer.writerow(valores)

except KeyboardInterrupt:
    print("Stopped by user")

# Close the connection to the serial port
porta_serial.close()