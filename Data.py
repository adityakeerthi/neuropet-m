import os 
import cv2
import numpy as np
import math
from Pixel import Pixel

def get_tracers():
    tracers = []
    for tracer in os.listdir("./Client"):
        tracers.append(tracer)
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

def RedMeanEuclidean(C1, C2):
    '''C1 and C2 represent RGB values of a colour. They are hashmaps in the form of {"R": r, "G": g, "B": b}, s.t. 0 <= r, g, b < 256.'''
    r̃ = (C1["R"] + C2["R"])/2
    Δr = abs(C1["R"] - C2["R"])
    Δg = abs(C1["G"] - C2["G"])
    Δb = abs(C1["B"] - C2["B"])
    
    '''https://en.wikipedia.org/wiki/Color_difference#sRGB'''
    return ( 
        math.sqrt(
            (Δr**2)*(2 + (r̃/256)) + 
            (Δg**2)*4 + 
            (Δb**2)*(2 + ((255 - r̃)/256))
        )
    )

def image_rgb():
    img = cv2.imread("./Client/AV45/AV45_r79SqA.jpg")
    print(img[0, 0])
    h, w = img.shape[:2]
    print(h, w)
    kp = {}
    for i in range(41, 169):
        c1 = { "R": img[i, 1514, 2], "G": img[i, 1514, 1], "B": img[i, 1514, 0] }
        kp[str(i)] = c1
    # for i in range(30, 178):
    #     c1 = { "R": img[i, 1511, 2], "G": img[i, 1511, 1], "B": img[i, 1511, 0] }
    #     print(c1)
    #     c2 = { "R": 0, "G": 0, "B": 0 }
    #     Δc = RedMeanEuclidean(c1, c2)
    #     print(Δc, img[i, 1511], i)
    print(kp)

def data_mining_OASIS3():
    '''This functions mine data from the combination of PET Scans (specifically from the OASIS3 dataset.'''
    tracers = get_tracers()
    dimensions = tuple([256, 256, 221])
    mined = [ [ [ None for _ in range(dimensions[0]) ] for _ in range(dimensions[1]) ] for _ in range(dimensions[2]) ]
    for row in range(6):
        for col in range(4):
            X = list(range(row*256, (row+1)*256))
            Y = list(range(col*256, (col+1)*256))
            for y in Y:
                for x in X:
                    pass
                    # if x <= row*256 + 40 and y <= col*256 + 40:
                    #     continue
                    # if 1497 <= x and x <= 1535 and (798 <= y and y <= 945 or 542 <= y and y <= 689 or 286 <= y and y <= 433 or 30 <= y and y <= 177):
                    #     continue
                    z = 14 + (row*6 + col)*9
                    print(x, y, z)
                    position = { "x": x, "y": y, "z": z }
                    if mined[x][y][z] == None:
                        mined[x][y][z] = Pixel(position, tracers)
                    # for tracer in tracers:
                    #     img = cv2.imread("./Client/" + tracer + "/" + tracer + "_r79SqA.jpg")
                    #     rgb = [img[x, y, 2], img[x, y, 1], img[x, y, 0]]
                    #     if rgb == [0, 0, 0]:
                    #         continue
                    #     c = mined[x][y][z].Add_Concentration(tracer, rgb)
        
    return True

mined = image_rgb()