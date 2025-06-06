# Import necessary libraries such as numpy, matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Function to extract the datapoints from the file, then return two lists(x,y) the coordinates
def collect(file):
    f = open(file,'r')
    x,y = [],[]
    for i in f:
        j = i.split()
        x.append(float(j[0])),y.append(float(j[1]))
    f.close()
    return x,y

# It constructs the matrix M of order len(x) times 2, the first column is filled with the x coordinates,
# second column is filled with ones
def matrixM(x):
    return np.column_stack([x,np.ones(len(x))])

# It returns the unknown parameters slope and intercept by using np.linalg.lstsq()
def l_sq_c_fit(M,y):
    (p1, p2), _, _, _ = np.linalg.lstsq(M, y, rcond=None)
    return p1,p2

# It returns a new list of y coordinates which are computed by using the etimated slope and intercept
def estimateline(x,m,c):
    y = []
    for i in x:
        y.append((m*i)+c)
    return y

x,y = collect('Datasets/dataset1.txt')
M = matrixM(x)
slope,intercept = l_sq_c_fit(M,y)
print(f"Slope of the Straight line is {slope}\nIntercept of the Straight line is {intercept}")

# 'esty' is the new list of y coordinates
esty = estimateline(x,slope,intercept)

# Plotting the curves
plt.plot(x,y,color = '#DEB887',label = "Original")
plt.plot(x,esty,color = '#00008B',label = "Estimated")
plt.title("Dataset-1")
plt.xlabel("X")
plt.ylabel("Y")
plt.errorbar(x[::25], y[::25], fmt='o-r',ms=3.5, mfc = "#8B0000", mec='#8B0000',label = "Error Bars")
plt.legend()
plt.savefig('dataset1.png')
