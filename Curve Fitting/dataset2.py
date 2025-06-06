#  Import necessary libraries such as numpy, matplotlib and scipy.optimize
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# It is a function which linearly interpolates the required value for the given points for an increasing curve
def inc_interp(x,xp,fp):
    interpvalues = [0]*len(x)
    for xi in x:
        for i in range(len(xp)-1):
            if xi>=xp[i] and xi<xp[i+1]:
                xp1,xp2 = xp[i],xp[i+1]
                fp1,fp2 = fp[i],fp[i+1]
                break
        value = fp1 + ((fp2-fp1)/(xp2-xp1))*(xi-xp1)
        interpvalues[x.index(xi)] += value
    return interpvalues

# # It is a function which linearly interpolates the required value for the given points for a deccreasing curve
def dec_interp(x,xp,fp):
    interpvalues = [0]*len(x)
    for xi in x:
        for i in range(len(xp)-1):
            if xi<=xp[i] and xi>xp[i+1]:
                xp1,xp2 = xp[i],xp[i+1]
                fp1,fp2 = fp[i],fp[i+1]
                break
        value = fp1 + ((fp2-fp1)/(xp2-xp1))*(xi-xp1)
        interpvalues[x.index(xi)] += value
    return interpvalues

# Function to extract the datapoints from the file, then return two lists(x,y) the coordinates
def collect(file):
    f = open(file,'r')
    x,y = [],[]
    for i in f:
        j = i.split()
        x.append(float(j[0])),y.append(float(j[1]))
    f.close()
    return x,y

# It returns the x coordinates where the value of y would become zero 
# It also returns the starting and ending points where curve_fit gives good approximation
def interp_xfy(x,y):
    i1,i2,i3 = 0,0,0
    for a in range(len(y)):
        if y[a]>0:
            i1+=a
            break
    for b in range(i1,len(y)):
        if y[b]<0:
            i2+=b
            break
    for c in range(i2,len(y)):
        if y[c]>0:
            i3+=c
            break
    p0 = inc_interp([0],y[:i1+1],x[:i1+1])[0]
    p1 = dec_interp([0],y[i1+1:i2+1],x[i1+1:i2+1])[0]
    p2 = inc_interp([0],y[i2+1:i3+1],x[i2+1:i3+1])[0]
    p3 = dec_interp([0],y[i3+1:],x[i3+1:])[0]
    p4 = inc_interp([0],y[::-1],x[::-1])[0]
    return p0,p1,p2,p3,p4,470,650

# It returns the amplitudes of sine waves by usign least squares regression
# Assuming the frequencies are in the ration 1:3:5, frequency = 2*pi/period 
def amp(x,y,p):
    t1,t2,t3 = 2*np.pi/p, 6*np.pi/p, 10*np.pi/p
    M = np.column_stack([np.sin(t1*np.array(x)),np.sin(t2*np.array(x)),np.sin(t3*np.array(x))])
    (a1,a2,a3),_,_,_ = np.linalg.lstsq(M,y,rcond=None)
    return a1,a2,a3

# It returns the amplitudes of sine waves along with the frequency
# It uses curve_fit to approximate the unknown values
def sinfunc(x,p1,a1,a2,a3):
    return a1*np.sin(p1*x)+a2*np.sin(3*p1*x)+a3*np.sin(5*p1*x)

x,y = collect("Datasets/ee22b022/Datasets/dataset2.txt")
p = interp_xfy(x,y)

# Calculation of periodicty
# The periodicty is defined as the distance between two consecutive crests or troughs, based on this the 
# equation for period is written
# Amplitudes are A1,A2,A3
period = ((p[1]-p[0])+(p[2]-p[1])+(p[3]-p[2])+(p[4]-p[3]))*0.5
t1,t2,t3 = 2*np.pi/period, 6*np.pi/period, 10*np.pi/period
A1,A2,A3 = amp(x,y,period)

print(f"Estimated Equations using Least Squares: {A1}*sin({t1}*x) + {A2}*sin({t2}*x) + {A3}*sin({t3}*x)")

# Boundaries for the dataset where the curve_fit gives good estimations
i1,i2 = p[5],p[6]
(period_cfit,A1_cfit,A2_cfit,A3_cfit),pcov = curve_fit(sinfunc,x[i1+1:i2],y[i1+1:i2])
print(f"Estimated Equation using Curve Fitting: {A1_cfit}*sin({period_cfit}*x) + {A2_cfit}*sin({3*period_cfit}*x) + {A3_cfit}*sin({5*period_cfit}*x)")

# New list of data points formed by putting the estimated values into the equation for signal
# expy_fls : By Least Squares, expy_fcf : By curve_fit
expy_fls, expy_fcf = [],[]
for i in x:
    e1 = A1*np.sin(t1*i)+A2*np.sin(t2*i)+A3*np.sin(t3*i)
    e2 = A1_cfit*np.sin(period_cfit*i)+A2_cfit*np.sin(3*period_cfit*i)+A3_cfit*np.sin(5*period_cfit*i)
    expy_fls.append(e1)
    expy_fcf.append(e2)

# Plotting three curves in a single plot
plt.plot(x,y,color = "#DEB887",label="Original")
plt.plot(x,expy_fls,color = "#00008B",label="Least Squares")
plt.plot(x,expy_fcf,color = "#DC143C",label="Curve Fitting")
plt.title("Dataset-2")
plt.xlabel('Time')
plt.ylabel('Y(t)')
plt.legend()
plt.savefig('dataset2.png')