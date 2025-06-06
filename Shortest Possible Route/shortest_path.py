# Importing the necessary libraries
import numpy as np
import sys
import matplotlib.pyplot as plt

# Initialize empty lists for x and y coordinates
x,y = [],[]
num = 0

# Open the file specified as a command line argument for reading and extracting the data from it
file = open(sys.argv[1],"r")
for line in file:
    words = line.split()
    if len(words) == 1:
        num += int(words[0])
    else:
        x.append(float(words[0]))
        y.append(float(words[1]))
file.close()
x,y = np.array(x),np.array(y)

# Function to calculate the Euclidean distance between two cities
def distancebwpts(city1,city2):
    x1, y1 = city1
    x2, y2 = city2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Function to calculate the total distance of a path through all cities
def distance(cities,cityorder):
    return sum(distancebwpts(cities[cityorder[i]], cities[cityorder[(i + 1) % len(cityorder)]]) for i in range(len(cityorder)))

# Function to find a solution to the Traveling Salesman Problem using Nearest Neighbour algorithm

def tsp(cities):
    num_cities = num

    # Initializing remaining cities list to keep track of unvisited cities.
    remaining_cities = list(range(num))

    # Choosing any random city as starting point
    initial_city = np.random.choice(remaining_cities) 

    # "tour" list contains the best order of cities  
    tour = [initial_city]
    remaining_cities.remove(initial_city)

    # tour list gets updates with the city which is nearest to the last appended city
    while remaining_cities:
        current_city = tour[-1]
        nearest_city = min(remaining_cities, key=lambda city: distancebwpts(cities[current_city], cities[city]))
        tour.append(nearest_city)
        remaining_cities.remove(nearest_city)
    return tour

cities = list(zip(x,y))

# Generate a random city order
rand_order = np.arange(num)
np.random.shuffle(rand_order)
dist_rand = distance(cities,rand_order)

# Extract x and y coordinates in the random order
x_rand,y_rand = np.array(x)[rand_order],np.array(y)[rand_order]
x_rand = np.append(x_rand,x_rand[0])
y_rand = np.append(y_rand,y_rand[0])

# Plot the random path
plt.plot(x_rand,y_rand,'o-',label="Random Path",color="#00008B")
plt.scatter([x_rand[0]],[y_rand[0]],label="Starting Point",s=120,color="#DC143C")
plt.xlabel("X"),plt.ylabel("Y")
plt.legend()
plt.title(f"Total Distance = {dist_rand}")
plt.show()
print(f"Randomly Generated City Order:\n{list(rand_order)}")
print(f"Total Distance: {dist_rand}")

city_orders,distances = [],[]
first_order = tsp(cities)
city_orders.append(first_order)
distances.append(distance(cities,first_order))

# Performing a local search to potentially find shorter paths
for i in range(50):
    order = tsp(cities)
    dist = distance(cities,order)
    if distances[-1] >= dist:
        city_orders.append(order)
        distances.append(dist)

# Extract the shortest path and its distance
short_path = city_orders[-1]
short_dist = distances[-1]
x_short,y_short = np.array(x)[short_path],np.array(y)[short_path]
x_short = np.append(x_short,x_short[0])
y_short = np.append(y_short,y_short[0])

# Plot the shortest path
plt.plot(x_short,y_short,'o-',label="Shortest Path",color="#D2691E")
plt.scatter([x_short[0]],[y_short[0]],label="Starting Point",s=120,color="#4B0082")
plt.xlabel("X"),plt.ylabel("Y")
plt.legend()
plt.title(f"Shortest Total Distance = {short_dist}")
plt.show()
print(f"City Order with Shortest Distance:\n{list(short_path)}")
print(f"Shortest Total Distance: {short_dist}")

# Percentage Improvement achieved by the Nearest Neighbour solution compared to the random order by comparing the distances
print(f"Percentage Improvement in the Path: {round((1-(short_dist/dist_rand))*100,4)}%")
