import serial
import matplotlib.pyplot as plt

# Serial Port Settings
porta_serial = serial.Serial('COM9', baudrate=9600)

try:
    while True:
        # Read data from serial port
        dados = porta_serial.readline().decode('utf-8').strip()
        
        # If the data is not empty
        if dados:
            plt.plot(dados)

except KeyboardInterrupt:
    print("Stopped by user")

# Close the connection to the serial port
porta_serial.close()