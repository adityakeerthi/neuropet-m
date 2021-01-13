import os 
import cv2
import numpy as np

def get_tracers():
    tracers = []
    for folder in os.listdir("./Client"): # Images will be inputted through the ./Client folder.
        tracers.append(folder) # Each folder in ./Client must be named accordingly to it's radioactive tracer. i.e. 'AV45', 'PIB'.
    return tracers

def get_scans():
    scans = {}
    tracers = get_tracers()
    for tracer in tracers:
        scans[tracer] = []
        for scan in os.listdir("./Client/" + tracer): 
            if scan != tracer + "_r79SqA.jpg":
                scans[tracer].append(scan) # Keeping track of each scan with it's tracer in a hashmap.
    return scans

def produce_concatenated_scans():
    scans = get_scans()
    for tracer in scans.keys():
        cv2_scans = []
        for scan in scans[tracer]:
            cv2_scans.append(cv2.imread("./Client/" + tracer + "/" + scan))
        if len(cv2_scans) > 0:
            concatenated_scan = cv2.vconcat(cv2_scans)
            cv2.imwrite("./Client/" + tracer + "/" + tracer + "_r79SqA.jpg", concatenated_scan)
    return True


print(get_scans())