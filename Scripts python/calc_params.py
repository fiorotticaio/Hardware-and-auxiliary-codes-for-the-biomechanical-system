import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import signal, fftpack
from scipy.signal import savgol_filter
import os 
from scipy.io import savemat
import pandas as pd
from sklearn.linear_model import LinearRegression
import csv
import os
import sys

import pandas as pd;

def rolling_rms(x, N):
  return (pd.DataFrame(abs(x)**2).rolling(N).mean()) **0.5

def fit_data(x,y):
    return LinearRegression().fit(x,y)

def get_linear_fit(model):
    return model.intercept_, model.coef_


ch1_f = []
ch2_f = []
ch1_e = []
ch2_e = []


file_name_flex = 'flexion.csv'

# Separate data that is separated by a comma
with open(file_name_flex, 'r') as arquivo_csv:
    csv_reader = csv.reader(arquivo_csv, delimiter=';')
    
    for line in csv_reader:
        n1, n2 = map(lambda x: float(x.replace(',', '.')), line[0].split(',')) # Convert comma to period
        # n1, n2 = map(lambda x: float(x.replace(',', '.')), line) # Convert comma to period
        # n1, n2 = map(float, line)
        ch1_f.append(n1)
        ch2_f.append(n2)


file_name_ext = 'extension.csv'

with open(file_name_ext, 'r') as arquivo_csv:
    csv_reader = csv.reader(arquivo_csv, delimiter=';')
    
    for line in csv_reader:
        n1, n2 = map(lambda x: float(x.replace(',', '.')), line[0].split(',')) # Convert comma to period
        # n1, n2 = map(lambda x: float(x.replace(',', '.')), line) # Convert comma to period
        # n1, n2 = map(float, line)
        ch1_e.append(n1)
        ch2_e.append(n2)


# Reshape data to be a column vector
ch1_f = np.array(ch1_f).reshape(len(ch1_f), 1)
ch2_f = np.array(ch2_f).reshape(len(ch2_f), 1)
ch1_e = np.array(ch1_e).reshape(len(ch1_e), 1)
ch2_e = np.array(ch2_e).reshape(len(ch2_e), 1)

# Get max values
max_ch1 = max(np.concatenate((ch1_f,ch1_e)))
max_ch2 = max(np.concatenate((ch2_f,ch2_e)))

# Get min values
min_ch1 = min(np.concatenate((ch1_f,ch1_e)))
min_ch2 = min(np.concatenate((ch2_f,ch2_e)))

# Normalize data to plot
x_f = (ch2_f - min_ch2)/(max_ch2 - min_ch2)
y_f = (ch1_f - min_ch1)/(max_ch1 - min_ch1)

# Normalize data to plot
x_e = (ch2_e - min_ch2)/(max_ch2 - min_ch2)
y_e = (ch1_e - min_ch1)/(max_ch1 - min_ch1)

# Fit data
model_flex = fit_data(x_f, y_f)
model_ext = fit_data(x_e, y_e)

# Get linear and angular coefficients 
b_flex, a_flex = get_linear_fit(model_flex)

# Create a vector to plot the linear fit
x_fit_f = np.linspace(0, 1, 100).reshape(-1, 1)
y_fit_f = 0 + a_flex * x_fit_f

# Get linear and angular coefficients
b_ext, a_ext = get_linear_fit(model_ext)

# Create a vector to plot the linear fit
x_fit_e = np.linspace(0, 1, 100).reshape(-1, 1)
y_fit_e = 0 + a_ext * x_fit_e

# Parse numpy array into float number
mf = a_flex[0]
mf = mf[0]
me = a_ext[0]
me = me[0]

m0 = math.tan((math.atan(mf)+math.atan(me))/2)

# Create a vector to plot the linear fit
x_fit_0 = np.linspace(0, 1, 100).reshape(-1, 1)
y_fit_0 = 0 + m0 * x_fit_0

uf_max = max_ch1[0]
ue_max = max_ch2[0]
uf_min = min_ch1[0]
ue_min = min_ch2[0]
vel_max = 70
K_max = 7

# print(f"11.24,0.41,1.36,6.98,8.04,2.23,2.28,80,7") # Test
print(f"{mf},{me},{m0},{uf_max},{ue_max},{uf_min},{ue_min},{vel_max},{K_max}")


# Plot
plt.figure()
#plt.plot(ch1_f)
#plt.plot(ch2_f)
#plt.plot(ch1_e)
#plt.plot(ch2_e)
plt.scatter(x_f, y_f, color='r', edgecolors='k', marker="*", linewidths=0.1)
plt.scatter(x_e, y_e, color='b', edgecolors='k''', marker="*", linewidths=0.1)
plt.plot(x_fit_f, y_fit_f, color='red', label='Linear Fit')
plt.plot(x_fit_e, y_fit_e, color='blue', label='Linear Fit')
plt.plot(x_fit_0, y_fit_0, color='green', label='Linear Fit')
# plt.title("Co-contraction Map")
# plt.xlabel("EMG(extension) activation")
# plt.ylabel("EMG(flexion) activation")
plt.xlim([-0.1,1.1])
plt.ylim([-0.1,1.1])
plt.show()