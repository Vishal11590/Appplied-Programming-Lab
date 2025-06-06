# Import necessary libraries such as numpy, matplotlib and scipy.optimize
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Declaring the values for c and T(estimated in the first part) only
c,T = 2.998e8, 4970.775990058394

# Function to extract the datapoints from the file, then return two lists(x,y) the coordinates
def collect(file):
    f = open(file,'r')
    x,y = [],[]
    for i in f:
        j = i.split()
        x.append(float(j[0])),y.append(float(j[1]))
    f.close()
    return x,y

# It return the estimated values of h and kb by using curve_fit with appropriate boundaries
def esthk(f,B):
    def func(f,h,k):
        num = (2*h*(f**3))/(c**2)
        den = np.exp((h*f)/(k*T))-1
        return num/den
    h,k = curve_fit(func,f,B,p0=[6.62607015e-34, 1.380649e-23])
    return h,k

freq,B = collect('Datasets/dataset3.txt')

# Appropriate boundaries for the dataset where the curve_fit will give better estimations
start = 2201
end = 2900
fmod = freq[start:end]
Bmod = B[start:end]

(h,kb),pcov = esthk(fmod,Bmod)

print(f"Estimated value of Planck's Constant is {h}")
print(f"Estimated value of Boltzmann Constant is {kb}")

# New list of intensities by putting the estimated h and kb into the intensity equation
expy = []
for i in range(len(freq)):
    a1,b1 = (2*h*(freq[i]**3))/(c**2), np.exp((h*freq[i])/(kb*T))-1
    expy.append(a1/b1)

# First Part Plotting
# New list of intensities by putting the temperature estimated into the intensity equation
estB = []
for i in freq:
    num = (2*6.62607015e-34*i*i*i)/(2.998e8**2)
    den = (np.exp((6.62607015e-34*i)/(1.380649e-23*T))-1)
    estB.append(num/den)

plt.plot(freq,B,color="#DEB887",label="Original")
plt.plot(freq,estB,color="#DC143C",label="Curve Fit, Part1")
plt.plot(freq,expy,label="Curve Fit, Part2",color="#665D1E")
plt.xlabel("Frequency")
plt.ylabel("Intensity of Black Body Radiation")
plt.title("Dataset-3")
plt.legend()
plt.savefig('dataset3.png')