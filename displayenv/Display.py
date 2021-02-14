from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time

start_time = time.time()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = []
y = []
z = []
c = []

file_read = open("./Client/AV45/Data/23.txt", "r")
for line in file_read:
    data = list(map(float, line[0:-2].split(", ")[:4]))
    print(data)
    x.append(data[0])
    y.append(data[1])
    z.append(data[2])
    c.append(data[3])

print("--- %s seconds ---" % (time.time() - start_time))

ax.scatter(x, y, z, c=c, cmap=plt.hot())
plt.show() 
