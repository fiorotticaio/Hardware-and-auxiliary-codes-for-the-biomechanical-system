# AUX FILE

file_path = 'C:/Users/Caio/UFES/Engenharia da Computação/7º Período/PIC-II/Virtual-Reality-Controlled-by-Myoelectric-Signals/Data/uData.csv'

curr_file_counter = 0
prev_file_counter = -1

# Abre o arquivo fora do loop
while True:
    try:
        file = open(file_path, 'r')
        break
    except FileNotFoundError:
        print("Arquivo não encontrado. Tentando novamente em alguns segundos...")

# Loop infinito para verificar se o arquivo foi modificados
while True:
    data = file.readline().strip().split(';')
    if data == ['']:
        data = None
    if data:
        curr_file_counter = int(data[0])
        if curr_file_counter > prev_file_counter:
            # print(data[0], data[1], data[2])
            print("Dado recebido do Unity:", data)
            prev_file_counter = curr_file_counter