from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time
import os

cdef list get_data_paths(tracer):
    cdef list dpaths = []
    for info in os.listdir("../Client/" + tracer + "/Data"):
        dpaths.append("../Client/" + tracer + "/Data/" + info)
    return dpaths

cpdef list generate_scan_dataset(data_path):
    cdef list x = []
    cdef list y = []
    cdef list z = []
    cdef list c = []
    cdef list data = []
    cdef list dset = [[], [], [], []]

    file_read = open(data_path, "r")
    for line in file_read:
        data = list(map(float, line[0:-2].split(", ")[:4]))
        x.append(data[0])
        y.append(data[1])
        z.append(data[2])
        c.append(data[3])
    
    dset[0] = x
    dset[1] = y
    dset[2] = z
    dset[3] = c

    return dset

cpdef list generate_dataset(tracer):
    cdef list dpaths = get_data_paths(tracer)
    cdef list x = []
    cdef list y = []
    cdef list z = []
    cdef list c = []
    cdef list dset = []
    cdef list total_data = [[], [], [], []]

    for data_path in dpaths:
        dset = generate_scan_dataset(data_path)
        x += dset[0]
        y += dset[1]
        z += dset[2]
        c += dset[3]
    
    total_data[0] = x
    total_data[1] = y
    total_data[2] = z
    total_data[3] = c

    return total_data