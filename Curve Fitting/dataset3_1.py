# Import necessary libraries such as numpy, matplotlib and scipy.optimize
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Declaring the values for Planck's,Boltzmann's constants and speed of light
h = 6.62607015e-34
kb = 1.380649e-23
c = 2.998e8

# Function to extract the datapoints from the file, then return two lists(x,y) the coordinates
def collect(file):
    f = open(file,'r')
    x,y = [],[]
    for i in f:
        j = i.split()
        x.append(float(j[0])),y.append(float(j[1]))
    f.close()
    return x,y

# It estimates the temperature at which the given data is simulated by using curve_fit
# Equation for temperature is mentioned in the documentation
def estT(f,B):
    B1 = []
    for i in range(len(B)):
        b = (2*h*(f[i]**3))/(c*c*B[i])
        B1.append(np.log(b+1))
    def func(t,T):
        return (h*t)/(kb*T)
    T,pcov = curve_fit(func,f,B1)
    return T[0]

freq,B = collect('Datasets/dataset3.txt')

# Appropriate boundaries for the dataset where the curve_fit will give better estimations
start = 1655
end = 2944
fmod = freq[start:end]
Bmod = B[start:end]
    
T = estT(fmod,Bmod)

# New list of intensities by putting the temperature estimated into the intensity equation
estB = []
for i in freq:
    num = (2*h*i*i*i)/(c*c)
    den = (np.exp((h*i)/(kb*T))-1)
    estB.append(num/den)

print(f"Estimated Temperature at which data is simulated is {T} Kelvin")

# Plotting the curves
plt.plot(freq,B,color="#DEB887",label="Original")
plt.plot(freq,estB,color="#DC143C",label="Curve Fitting")
plt.xlabel("Frequency")
plt.ylabel("Intensity of Black Body Radiation")
plt.title("Dataset-3")
plt.legend()
plt.savefig('dataset3_1.png')