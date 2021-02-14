from Display import generate_dataset, generate_scan_dataset
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time
import concurrent.futures
import os

start_time = time.time()

# def get_data_list(tracer):
#     dlist = []
#     for info in os.listdir("../Client/" + tracer + "/Data"):
#         dlist.append("../Client/" + tracer + "/Data/" + info)
#     return dlist

# dlist = get_data_list("AV45")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# dset = generate_scan_dataset(dlist[0])
dset = generate_dataset()
# ../Client/AV45/Data/23.txt
print("--- %s seconds ---" % (time.time() - start_time))

ax.scatter(dset[0], dset[1], dset[2], c=dset[3], cmap=plt.hot())
plt.show() 