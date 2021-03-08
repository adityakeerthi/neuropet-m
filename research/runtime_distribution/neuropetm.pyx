import cv2
import os
import math
import numpy as np
import pandas as pd
import plotly.express as px
import datetime
import json
import time

# Crop and reorganize PET Scans named by their depths
cpdef produce_scans_OASIS3(client):
    cdef int scan_x, scan_y, H, W, Channels, _yPlus, _x, _xPlus
    for tracer in os.listdir("./tests/" + client):
        if "." in tracer: continue
        if "Scans" not in os.listdir("./tests/" + client + "/" + tracer): os.makedirs("./tests/" + client + "/" + tracer + "/Scans")
        if "Data" not in os.listdir("./tests/" + client + "/" + tracer): os.makedirs("./tests/" + client + "/" + tracer + "/Data")

        for file_name in os.listdir("./tests/" + client + "/" + tracer + "/Scans"):
            os.remove("./tests/" + client + "/" + tracer + "/Scans/" + file_name)

        for file_name in os.listdir("./tests/" + client + "/" + tracer + "/Data"):
            os.remove("./tests/" + client + "/" + tracer + "/Data/" + file_name)

        scan_x, scan_y = 0, 0
        for scan in os.listdir("./tests/" + client + "/" + tracer):
            if ".jpg" not in scan: continue
            scan_path = "./tests/" + client + "/" + tracer + "/" + scan
            img = cv2.imread(scan_path)
            H, W, Channels = img.shape
            for x in range(30, 178):
                for y in range(1497, 1536):
                    img.itemset((x, y, 0), 0)
                    img.itemset((x, y, 1), 0)
                    img.itemset((x, y, 2), 0)
            for j in range(6):
                for x in range(0, 20):
                    for y in range(j*256, j*256 + 30):
                        img.itemset((x, y, 0), 0)
                        img.itemset((x, y, 1), 0)
                        img.itemset((x, y, 2), 0)
            temp_img = img
            for xIncrement in range(6):
                scan_x %= 6
                _yPlus = int(H)
                _x = int(W / 6 * xIncrement)   
                _xPlus = int(W / 6)
                img = img[0:_yPlus, _x:_x+_xPlus]
                file_name = 14+(scan_y*6 + scan_x)*9
                cropped_image_path = "./tests/" + client + "/" + tracer + "/Scans/" + str(file_name) + ".jpg"
                cv2.imwrite(cropped_image_path, img)
                img = temp_img
                scan_x += 1
            scan_y += 1

# RedMeanEuclidean utilized in RGB_to_Concentration
cdef double RedMeanEuclidean(dict C1, dict C2):
    cdef double rAverage = (C1["R"] + C2["R"])/2
    cdef double rD = abs(C1["R"] - C2["R"])
    cdef double gD = abs(C1["G"] - C2["G"])
    cdef double bD = abs(C1["B"] - C2["B"])

    return ( 
        math.sqrt(
            (rD**2.0)*(2.0 + (rAverage/256.0)) + 
            (gD**2.0)*4.0 + 
            (bD**2.0)*(2.0 + ((255.0 - rAverage)/256.0))
        )
    )

# RGB_to_Concentration to map each pixel on the PET Scans
cdef double RGB_to_Concentration(list rgb):
    # Mined pixels representing the concentration value at a specific RGB arrangement
    cdef dict mined = {'41': {'R': 166, 'G': 33, 'B': 28}, '42': {'R': 198, 'G': 19, 'B': 12}, '43': {'R': 204, 'G': 19, 'B': 0}, '44': {'R': 212, 'G': 61, 'B': 14}, '45': {'R': 199, 'G': 74, 'B': 8}, '46': {'R': 181, 'G': 71, 'B': 0}, '47': {'R': 183, 'G': 76, 'B': 0}, '48': {'R': 182, 'G': 69, 'B': 0}, '49': {'R': 186, 'G': 70, 'B': 0}, '50': {'R': 187, 'G': 71, 'B': 0}, '51': {'R': 208, 'G': 95, 'B': 17}, '52': {'R': 214, 'G': 101, 'B': 23}, '53': {'R': 206, 'G': 95, 'B': 14}, '54': {'R': 213, 'G': 107, 'B': 21}, '55': {'R': 202, 'G': 101, 'B': 11}, '56': {'R': 202, 'G': 103, 'B': 10}, '57': {'R': 229, 'G': 135, 'B': 39}, '58': {'R': 225, 'G': 133, 'B': 34}, '59': {'R': 220, 'G': 133, 'B': 30}, '60': {'R': 222, 'G': 137, 'B': 31}, '61': {'R': 214, 'G': 131, 'B': 25}, '62': {'R': 217, 'G': 136, 'B': 28}, '63': {'R': 206, 'G': 136, 'B': 24}, '64': {'R': 232, 'G': 183, 'B': 65}, '65': {'R': 228, 'G': 189, 'B': 68}, '66': {'R': 220, 'G': 186, 'B': 63}, '67': {'R': 224, 'G': 194, 'B': 70}, '68': {'R': 219, 'G': 194, 'B': 68}, '69': {'R': 217, 'G': 198, 'B': 70}, '70': {'R': 232, 'G': 217, 'B': 88}, '71': {'R': 226, 'G': 216, 'B': 84}, '72': {'R': 228, 'G': 221, 'B': 88}, '73': {'R': 229, 'G': 225, 'B': 89}, '74': {'R': 226, 'G': 224, 'B': 87}, '75': {'R': 221, 'G': 222, 'B': 84}, '76': {'R': 226, 'G': 227, 'B': 87}, '77': {'R': 238, 'G': 239, 'B': 99}, '78': {'R': 244, 'G': 245, 'B': 105}, '79': {'R': 242, 'G': 244, 'B': 101}, '80': {'R': 240, 'G': 240, 'B': 92}, '81': {'R': 234, 'G': 244, 'B': 85}, '82': {'R': 220, 'G': 249, 'B': 69}, '83': {'R': 211, 'G': 248, 'B': 54}, '84': {'R': 209, 'G': 249, 'B': 41}, '85': {'R': 208, 'G': 251, 'B': 37}, '86': {'R': 203, 'G': 252, 'B': 36}, '87': {'R': 197, 'G': 252, 'B': 39}, '88': {'R': 197, 'G': 255, 'B': 59}, '89': {'R': 176, 'G': 255, 'B': 67}, '90': {'R': 104, 'G': 226, 'B': 37}, '91': {'R': 87, 'G': 235, 'B': 51}, '92': {'R': 69, 'G': 230, 'B': 54}, '93': {'R': 76, 'G': 242, 'B': 74}, '94': {'R': 68, 'G': 235, 'B': 70}, '95': {'R': 78, 'G': 235, 'B': 82}, '96': {'R': 78, 'G': 209, 'B': 77}, '97': {'R': 88, 'G': 208, 'B': 84}, '98': {'R': 86, 'G': 204, 'B': 81}, '99': {'R': 89, 'G': 204, 'B': 83}, '100': {'R': 80, 'G': 194, 'B': 73}, '101': {'R': 87, 'G': 198, 'B': 80}, '102': {'R': 91, 'G': 200, 'B': 85}, '103': {'R': 54, 'G': 157, 'B': 48}, '104': {'R': 50, 'G': 148, 'B': 45}, '105': {'R': 63, 'G': 154, 'B': 58}, '106': {'R': 58, 'G': 143, 'B': 52}, '107': {'R': 70, 'G': 148, 'B': 64}, '108': {'R': 68, 'G': 139, 'B': 61}, '109': {'R': 48, 'G': 111, 'B': 40}, '110': {'R': 48, 'G': 107, 'B': 39}, '111': {'R': 48, 'G': 102, 'B': 40}, '112': {'R': 57, 'G': 108, 'B': 51}, '113': {'R': 62, 'G': 110, 'B': 58}, '114': {'R': 59, 'G': 105, 'B': 59}, '115': {'R': 61, 'G': 99, 'B': 86}, '116': {'R': 123, 'G': 147, 'B': 195}, '117': {'R': 125, 'G': 140, 'B': 223}, '118': {'R': 124, 'G': 133, 'B': 226}, '119': {'R': 129, 'G': 135, 'B': 233}, '120': {'R': 130, 'G': 132, 'B': 232}, '121': {'R': 135, 'G': 135, 'B': 233}, '122': {'R': 114, 'G': 113, 'B': 207}, '123': {'R': 117, 'G': 113, 'B': 207}, '124': {'R': 121, 'G': 117, 'B': 212}, '125': {'R': 115, 'G': 112, 'B': 203}, '126': {'R': 123, 'G': 121, 'B': 204}, '127': {'R': 120, 'G': 119, 'B': 199}, '128': {'R': 125, 'G': 123, 'B': 207}, '129': {'R': 107, 'G': 104, 'B': 191}, '130': {'R': 101, 'G': 98, 'B': 185}, '131': {'R': 104, 'G': 101, 'B': 188}, '132': {'R': 104, 'G': 102, 'B': 186}, '133': {'R': 107, 'G': 106, 'B': 186}, '134': {'R': 102, 'G': 102, 'B': 176}, '135': {'R': 83, 'G': 84, 'B': 151}, '136': {'R': 91, 'G': 93, 'B': 154}, '137': {'R': 83, 'G': 86, 'B': 141}, '138': {'R': 85, 'G': 88, 'B': 141}, '139': {'R': 79, 'G': 82, 'B': 133}, '140': {'R': 83, 'G': 86, 'B': 139}, '141': {'R': 80, 'G': 83, 'B': 138}, '142': {'R': 55, 'G': 57, 'B': 114}, '143': {'R': 52, 'G': 52, 'B': 112}, '144': {'R': 57, 'G': 55, 'B': 118}, '145': {'R': 57, 'G': 55, 'B': 118}, '146': {'R': 57, 'G': 58, 'B': 115}, '147': {'R': 52, 'G': 58, 'B': 110}, '148': {'R': 49, 'G': 57, 'B': 104}, '149': {'R': 48, 'G': 55, 'B': 97}, '150': {'R': 50, 'G': 55, 'B': 93}, '151': {'R': 56, 'G': 54, 'B': 93}, '152': {'R': 55, 'G': 43, 'B': 83}, '153': {'R': 65, 'G': 39, 'B': 84}, '154': {'R': 74, 'G': 31, 'B': 85}, '155': {'R': 77, 'G': 19, 'B': 80}, '156': {'R': 82, 'G': 9, 'B': 80}, '157': {'R': 92, 'G': 5, 'B': 84}, '158': {'R': 99, 'G': 3, 'B': 90}, '159': {'R': 92, 'G': 6, 'B': 79}, '160': {'R': 73, 'G': 17, 'B': 56}, '161': {'R': 30, 'G': 0, 'B': 15}, '162': {'R': 23, 'G': 0, 'B': 11}, '163': {'R': 14, 'G': 0, 'B': 9}, '164': {'R': 5, 'G': 0, 'B': 5}, '165': {'R': 2, 'G': 2, 'B': 4}, '166': {'R': 3, 'G': 3, 'B': 3}, '167': {'R': 0, 'G': 0, 'B': 0}, '168': {'R': 1, 'G': 1, 'B': 0}}
    cdef double mincur, cD
    cdef int lvl = 0
    cdef dict c1, c2
    mincur, cD = -1.0, 0.0
    for level in mined:
        c1 = { "R": rgb[0], "G": rgb[1], "B": rgb[2] }
        c2 = { "R": mined[level]["R"], "G" : mined[level]["G"], "B": mined[level]["B"] }
        cD = RedMeanEuclidean(c1, c2)
        if mincur == -1 or cD < mincur:
            mincur = cD
            lvl = int(level)
    cdef double concentration = round((168.0-lvl)/64.0, 1)
    return concentration

# Function extrapolating data from a given PET Scan input path
cpdef process_scan_path(scan_path):
    client = scan_path.split("/")[2]
    tracer = scan_path.split("/")[3]
    depth = scan_path.split("/")[5].split(".")[0]
    file_write = open("./tests/" + client + "/" + tracer + "/Data/" + depth + ".txt", "w+")
    Scan = cv2.imread(scan_path)
    
    cdef int H, W, Channels
    cdef list concentrations, rgb 
    cdef double concentration, lower_threshold, higher_threshold

    concentration = 0.0
    H, W, Channels = Scan.shape

    for x in range(H):
        for y in range(W):
            rgb = [Scan.item(x, y, 2), Scan.item(x, y, 1), Scan.item(x, y, 0)]
            concentration = RGB_to_Concentration(rgb)
            if 1.5 <= concentration and concentration <= 2.0:
                data = "{x}, {y}, {z}, {concentration} \n".format(x=x, y=y, z=depth, concentration=concentration)
                file_write.write(data)
    file_write.close()
    return True

cdef Concentration_to_RGB(double concentration, legend, tracer):
    cdef dict mined = {
        "blues": {638: {'R': 8, 'G': 48, 'B': 107}, 606: {'R': 8, 'G': 61, 'B': 126}, 574: {'R': 8, 'G': 74, 'B': 146}, 542: {'R': 13, 'G': 87, 'B': 161}, 510: {'R': 23, 'G': 100, 'B': 171}, 478: {'R': 33, 'G': 113, 'B': 181}, 446: {'R': 46, 'G': 126, 'B': 187}, 414: {'R': 59, 'G': 139, 'B': 194}, 382: {'R': 74, 'G': 151, 'B': 201}, 350: {'R': 91, 'G': 163, 'B': 207}, 318: {'R': 107, 'G': 174, 'B': 214}, 286: {'R': 128, 'G': 185, 'B': 218}, 254: {'R': 148, 'G': 196, 'B': 222}, 222: {'R': 166, 'G': 205, 'B': 228}, 190: {'R': 182, 'G': 212, 'B': 233}, 158: {'R': 198, 'G': 219, 'B': 239}, 126: {'R': 207, 'G': 225, 'B': 242}, 94: {'R': 217, 'G': 232, 'B': 245}, 62: {'R': 227, 'G': 238, 'B': 248}, 30: {'R': 237, 'G': 244, 'B': 251}},
        "greens": {637: {'R': 0, 'G': 69, 'B': 27}, 605: {'R': 0, 'G': 85, 'B': 34}, 573: {'R': 0, 'G': 102, 'B': 41}, 541: {'R': 8, 'G': 115, 'B': 49}, 509: {'R': 22, 'G': 128, 'B': 59}, 477: {'R': 36, 'G': 140, 'B': 69}, 445: {'R': 48, 'G': 152, 'B': 79}, 413: {'R': 60, 'G': 165, 'B': 89}, 381: {'R': 77, 'G': 176, 'B': 98}, 349: {'R': 97, 'G': 186, 'B': 108}, 317: {'R': 117, 'G': 196, 'B': 119}, 285: {'R': 135, 'G': 205, 'B': 134}, 253: {'R': 153, 'G': 213, 'B': 149}, 221: {'R': 170, 'G': 220, 'B': 163}, 189: {'R': 185, 'G': 227, 'B': 178}, 157: {'R': 200, 'G': 233, 'B': 193}, 125: {'R': 212, 'G': 238, 'B': 206}, 93: {'R': 224, 'G': 243, 'B': 218}, 61: {'R': 233, 'G': 246, 'B': 229}, 29: {'R': 240, 'G': 249, 'B': 237}},
        "oranges": {636: {'R': 127, 'G': 39, 'B': 3}, 604: {'R': 143, 'G': 45, 'B': 3}, 572: {'R': 158, 'G': 51, 'B': 3}, 540: {'R': 177, 'G': 57, 'B': 2}, 508: {'R': 197, 'G': 65, 'B': 1}, 476: {'R': 217, 'G': 72, 'B': 1}, 444: {'R': 227, 'G': 85, 'B': 8}, 412: {'R': 236, 'G': 99, 'B': 15}, 380: {'R': 243, 'G': 113, 'B': 28}, 348: {'R': 248, 'G': 127, 'B': 44}, 316: {'R': 253, 'G': 141, 'B': 61}, 284: {'R': 253, 'G': 155, 'B': 80}, 252: {'R': 253, 'G': 168, 'B': 98}, 220: {'R': 253, 'G': 181, 'B': 119}, 188: {'R': 253, 'G': 195, 'B': 141}, 156: {'R': 253, 'G': 208, 'B': 163}, 124: {'R': 253, 'G': 217, 'B': 180}, 92: {'R': 253, 'G': 226, 'B': 198}, 60: {'R': 254, 'G': 233, 'B': 212}, 28: {'R': 254, 'G': 239, 'B': 224}},
        "purples": {637: {'R': 63, 'G': 0, 'B': 125}, 605: {'R': 71, 'G': 16, 'B': 132}, 573: {'R': 80, 'G': 31, 'B': 139}, 541: {'R': 88, 'G': 48, 'B': 147}, 509: {'R': 97, 'G': 65, 'B': 155}, 477: {'R': 106, 'G': 81, 'B': 163}, 445: {'R': 115, 'G': 99, 'B': 172}, 413: {'R': 124, 'G': 117, 'B': 181}, 381: {'R': 134, 'G': 131, 'B': 189}, 349: {'R': 146, 'G': 143, 'B': 194}, 317: {'R': 158, 'G': 154, 'B': 200}, 285: {'R': 170, 'G': 168, 'B': 208}, 253: {'R': 182, 'G': 182, 'B': 216}, 221: {'R': 194, 'G': 195, 'B': 223}, 189: {'R': 206, 'G': 207, 'B': 229}, 157: {'R': 218, 'G': 218, 'B': 235}, 125: {'R': 227, 'G': 226, 'B': 239}, 93: {'R': 235, 'G': 233, 'B': 243}, 61: {'R': 241, 'G': 240, 'B': 246}, 29: {'R': 247, 'G': 245, 'B': 250}},
        "reds": {637: {'R': 104, 'G': 0, 'B': 13}, 605: {'R': 129, 'G': 6, 'B': 16}, 573: {'R': 153, 'G': 12, 'B': 19}, 541: {'R': 173, 'G': 16, 'B': 22}, 509: {'R': 188, 'G': 20, 'B': 25}, 477: {'R': 203, 'G': 24, 'B': 29}, 445: {'R': 218, 'G': 38, 'B': 35}, 413: {'R': 232, 'G': 52, 'B': 41}, 381: {'R': 241, 'G': 69, 'B': 50}, 349: {'R': 246, 'G': 88, 'B': 62}, 317: {'R': 251, 'G': 107, 'B': 75}, 285: {'R': 251, 'G': 123, 'B': 91}, 253: {'R': 251, 'G': 139, 'B': 107}, 221: {'R': 252, 'G': 155, 'B': 124}, 189: {'R': 252, 'G': 171, 'B': 143}, 157: {'R': 252, 'G': 188, 'B': 162}, 125: {'R': 252, 'G': 202, 'B': 182}, 93: {'R': 253, 'G': 217, 'B': 201}, 61: {'R': 254, 'G': 228, 'B': 216}, 29: {'R': 254, 'G': 237, 'B': 228}}
    }

    cdef double lower_threshold, higher_threshold, distance
    lower_threshold, higher_threshold = 1.5, 2.0
    distance = higher_threshold - lower_threshold
    concentration -= lower_threshold
    cdef int sigmoid = int(639.0*(concentration/distance))

    cdef int lvl, current_distance, minimum_distance
    cdef list rgb
    lvl, current_distance, minimum_distance = 0, 0, 640

    for level in mined[legend]:
        current_distance = abs(level-sigmoid)
        if current_distance < minimum_distance:
            minimum_distance = current_distance
            rgb = [mined[legend][level]["R"], mined[legend][level]["G"], mined[legend][level]["B"]]

    hexadecimal = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

    return hexadecimal

# Generating the Pandas dataset to be plotted on Plotly
cdef dict generate_pdset(client):
    cdef list data_paths, data_line, legends
    cdef dict data_dict, colour_discrete_map
    data_dict, colour_discrete_map = {"~x": [], "~y": [], "~z": [], "~keys": [], "~tracer": []}, {}
    cdef int i = 0
    legends = ["blues", "reds", "greens", "purples", "oranges"]
    legend, rgb = "", ""

    for tracer in os.listdir("./tests/" + client):
        if "." in tracer: continue
        legend = legends[i]
        data_paths, data_line = [], []
        for info in os.listdir("./tests/" + client + "/" + tracer + "/Data"):
            data_paths.append("./tests/" + client + "/" + tracer + "/Data/" + info)
        
        for data_path in data_paths:
            file_read = open(data_path, "r")
            for line in file_read:
                data_line = list(map(float, line[0:-2].split(", ")[:4]))
                rgb = Concentration_to_RGB(data_line[3], legend, tracer)
                colour_discrete_map.setdefault(str(data_line[3]) + " " + tracer, rgb)
                data_dict["~x"].append(data_line[0])
                data_dict["~y"].append(data_line[1])
                data_dict["~z"].append(data_line[2])
                data_dict["~keys"].append(str(data_line[3]) + " " + tracer)
                data_dict["~tracer"].append(tracer)

        i += 1

    data_dict["~colour_discrete_map"] = colour_discrete_map

    return data_dict

cpdef produce_multimodal_scan(client):
    cdef dict dataset, c_discrete_map
    cdef list x, y, z, keys, tracers

    dataset = generate_pdset(client)
    c_discrete_map = dataset["~colour_discrete_map"]
    x, y, z, keys, tracers = dataset["~x"], dataset["~y"], dataset["~z"], dataset["~keys"], dataset["~tracer"]

    fig = px.scatter_3d(x=x, y=y, z=z, color=keys, color_discrete_map=c_discrete_map, opacity=0.5, template="plotly_dark", title=client)

    fig.write_html("./NPETM.Scans/" + client + ".html")

    return True