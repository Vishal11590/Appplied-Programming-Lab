# Importing the necessary libraries which are used for plotting
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Polynomial Functions along with their gradient/s
def f1(x):
    return x**2 + 3*x + 8
def df1_dx(x):
    return 2*x + 3
def f3(x, y):
    return x**4 - 16*x**3 + 96*x**2 - 256*x + y**2 - 4*y + 262
def df3_dx(x, y):
    return 4*x**3 - 48*x**2 + 192*x - 256
def df3_dy(x, y):
    return 2*y - 4
def f4(x,y):
    return np.exp(-(x - y)**2) * np.sin(y)
def df4_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)
def df4_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)
def f5(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1
def df5_dx(x):
    return (-4)*(np.cos(x)**3)*np.sin(x) + (-3)*np.cos(x)*(np.sin(x)**2) + (-4)*np.sin(2*x) - np.sin(x)

# Assigning the ranges for optimization
x1 = np.linspace(-5,5,100)
x3,y3 = np.linspace(-10,10,100),np.linspace(-10,10,100)
x4,y4 = np.linspace(-np.pi,np.pi,100),np.linspace(-5,5,100)
x5 = np.linspace(0,2*np.pi,100)

# This function implements the gradient descent algorithm and finds the minima in the specified range
def gradient_descent_optimization(f,df,bounds,sx,lr=0.1,i=100,gap=50):

    # For 1D Polynomials
    if len(bounds) == 1:

        # Lists to store the path for optimization, for each iteration the path gets updated based on the 
        # equation "sx[0] -= df[0](sx[0])*lr".
        x_path,y_path = [],[]
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_xlabel("X"),ax.set_ylabel(f"{f.__name__}(X)")
        y = [f(a) for a in bounds[0]]

        # Plotting the graphs
        ax.plot(bounds[0],y,color='#191970',label=f"{f.__name__}(X)")

        # Highlighting the starting point
        ax.plot([sx[0]],[f(sx[0])],color='#FF1493',label='Starting Point',ms=11,marker='o')
        lnall, = ax.plot([],[],'o',color='#DC143C',label=f"Optimization Trajectory for {f.__name__}(X)")
        lngood, = ax.plot([],[],'o',color='#556B2F',ms=10,label="Point of Minima")

        # This function updates the trajectory
        def update1D(frame):
            nonlocal sx
            sx[0] -= df[0](sx[0])*lr
            y1 = f(sx[0])
            lngood.set_data([sx[0]],[y1])
            x_path.append(sx[0])
            y_path.append(y1)
            lnall.set_data(x_path,y_path)
            ax.set_title(f"Iteration {frame+1}: x = {round(sx[0],3)}, {f.__name__}(x) = {round(y1,3)}")
            return lngood,

        # Creating the animation showing how optimization is happening with the given learning rate
        ani = FuncAnimation(fig,update1D,frames=i,interval=gap,repeat=False)
        ax.legend()
        plt.show()

        # Printing the final optimized values after given number of iterations
        print(f"Optimal Solution for {f.__name__}(x) after {i} iterations:")
        print(f"x = {sx[0]}, {f.__name__}(x) = {f(sx[0])}")

    # For 2D Polynomials
    elif len(bounds) == 2:

        # Lists to store the path for optimization, for each iteration the path gets updated based on the 
        # equations "sx[0] -= lr*df[0](sx[0],sx[1], sx[1] -= lr*df[1](sx[0],sx[1])"
        x_path,y_path,z_path = [],[],[]

        # Plotting 3D Graphs
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.set_xlabel("X"),ax.set_ylabel("Y"),ax.set_zlabel(f"{f.__name__}(X,Y)")

        # Creating mesh grids
        X,Y = np.meshgrid(bounds[0],bounds[1])
        Z = f(X,Y)

        # Creating the surface
        surf = ax.plot_surface(X,Y,Z,cmap='coolwarm',alpha=0.8)

        # Highlighting the starting point
        ax.scatter(sx[0],sx[1],f(sx[0],sx[1]),label='Starting Point',color='#FF1493',s=50)
        sc = ax.scatter([],[],[],c='red',s=30,label=f"Optimization Trajectory for {f.__name__}(X,Y)")
        lngood, = ax.plot([],[],[],'o',color='#556B2F',ms=8,label="Point of Minima")

        # This function updates the trajectory after every iteration
        def update2D(frame):
            nonlocal sx
            x_path.append(sx[0])
            y_path.append(sx[1])
            z_path.append(f(sx[0],sx[1]))
            lngood.set_data([sx[0]],[sx[1]])
            lngood.set_3d_properties([f(sx[0],sx[1])])
            sx[0] -= lr*df[0](sx[0],sx[1])
            sx[1] -= lr*df[1](sx[0],sx[1])
            sc._offsets3d = (x_path,y_path,z_path)
            ax.set_title(f"Iteration {frame+1}: x = {round(sx[0],3)}, y = {round(sx[1],3)}, {f.__name__}(x,y) = {round(f(sx[0],sx[1]))}")

        # Creating Animation
        ani = FuncAnimation(fig,update2D,frames=i,interval=gap,repeat=False)
        ax.legend()
        plt.show()
        
        # Outputs the final optimized values
        print(f"Optimal Solution for {f.__name__}(x,y) after {i} iterations:")
        print(f"x = {sx[0]}, y = {sx[1]}, {f.__name__}(x,y) = {f(sx[0],sx[1])}")

# Examples
gradient_descent_optimization(f1,[df1_dx],[x1],[4.5])
gradient_descent_optimization(f3,[df3_dx,df3_dy],[x3,y3],[5,5],0.1,150,25)
gradient_descent_optimization(f4,[df4_dx,df4_dy],[x4,y4],[-0.1,-0.1],0.1,150,25)
gradient_descent_optimization(f5,[df5_dx],[x5],[0.2],0.05,100)
