import serial

# Serial Port Settings
serial_port = serial.Serial('COM19', baudrate=9600)

# Send data to Arduino
num = float(25.45)
serial_port.write(f'{num}'.encode())

# serial_port.close()