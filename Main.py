import cv2
import os
import math
import time

start_time = time.time()

def produce_scans_OASIS3():
    for tracer in os.listdir("./Client"):
        scan_x, scan_y = 0, 0
        for scan in os.listdir("./Client/" + tracer):
            if ".jpg" not in scan: continue
            scan_path = "./Client/" + tracer + "/" + scan
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
                cropped_image_path = "./Client/" + tracer + "/Scans/" + str(file_name) + ".jpg"
                if "Scans" not in os.listdir("./Client/" + tracer):
                    os.makedirs("./Client/" + tracer + "/Scans")
                if "Data" not in os.listdir("./Client/" + tracer):
                    os.makedirs("./Client/" + tracer + "/Data")
                cv2.imwrite(cropped_image_path, img)
                img = temp_img
                scan_x += 1
            scan_y += 1

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

def RGB_to_Concentration(rgb):
    mined = {'41': {'R': 166, 'G': 33, 'B': 28}, '42': {'R': 198, 'G': 19, 'B': 12}, '43': {'R': 204, 'G': 19, 'B': 0}, '44': {'R': 212, 'G': 61, 'B': 14}, '45': {'R': 199, 'G': 74, 'B': 8}, '46': {'R': 181, 'G': 71, 'B': 0}, '47': {'R': 183, 'G': 76, 'B': 0}, '48': {'R': 182, 'G': 69, 'B': 0}, '49': {'R': 186, 'G': 70, 'B': 0}, '50': {'R': 187, 'G': 71, 'B': 0}, '51': {'R': 208, 'G': 95, 'B': 17}, '52': {'R': 214, 'G': 101, 'B': 23}, '53': {'R': 206, 'G': 95, 'B': 14}, '54': {'R': 213, 'G': 107, 'B': 21}, '55': {'R': 202, 'G': 
    101, 'B': 11}, '56': {'R': 202, 'G': 103, 'B': 10}, '57': {'R': 229, 'G': 135, 'B': 39}, '58': {'R': 225, 'G': 133, 'B': 34}, '59': {'R': 220, 'G': 133, 'B': 30}, '60': {'R': 222, 'G': 137, 'B': 31}, '61': {'R': 214, 'G': 131, 'B': 25}, '62': {'R': 217, 'G': 136, 'B': 28}, '63': {'R': 206, 'G': 136, 'B': 24}, '64': {'R': 232, 'G': 183, 'B': 65}, 
    '65': {'R': 228, 'G': 189, 'B': 68}, '66': {'R': 220, 'G': 186, 'B': 63}, '67': {'R': 224, 'G': 194, 'B': 70}, '68': {'R': 219, 'G': 194, 'B': 68}, '69': {'R': 217, 'G': 198, 'B': 70}, '70': {'R': 232, 'G': 217, 'B': 88}, '71': {'R': 226, 'G': 216, 'B': 84}, '72': {'R': 228, 'G': 221, 'B': 88}, '73': {'R': 229, 'G': 225, 'B': 89}, '74': {'R': 226, 'G': 224, 'B': 87}, '75': {'R': 221, 'G': 222, 'B': 84}, '76': {'R': 226, 'G': 227, 'B': 87}, '77': {'R': 238, 'G': 239, 'B': 99}, '78': {'R': 244, 'G': 245, 'B': 105}, '79': {'R': 242, 'G': 244, 'B': 101}, '80': {'R': 240, 'G': 240, 'B': 92}, '81': {'R': 234, 'G': 244, 'B': 85}, '82': {'R': 220, 'G': 249, 'B': 69}, '83': {'R': 211, 'G': 248, 'B': 54}, '84': {'R': 209, 'G': 249, 'B': 41}, '85': {'R': 208, 'G': 251, 'B': 37}, '86': {'R': 203, 'G': 252, 'B': 36}, '87': {'R': 197, 'G': 252, 'B': 39}, '88': {'R': 197, 
    'G': 255, 'B': 59}, '89': {'R': 176, 'G': 255, 'B': 67}, '90': {'R': 104, 'G': 226, 'B': 37}, '91': {'R': 87, 'G': 235, 'B': 51}, '92': {'R': 69, 'G': 230, 'B': 54}, '93': {'R': 76, 'G': 242, 'B': 74}, '94': {'R': 68, 'G': 235, 'B': 70}, '95': {'R': 78, 'G': 235, 'B': 82}, '96': {'R': 78, 'G': 209, 'B': 77}, '97': {'R': 88, 'G': 208, 'B': 84}, '98': {'R': 86, 'G': 204, 'B': 81}, '99': {'R': 89, 'G': 204, 'B': 83}, '100': {'R': 80, 'G': 194, 'B': 73}, '101': {'R': 87, 'G': 198, 'B': 80}, '102': {'R': 91, 'G': 200, 'B': 85}, '103': {'R': 54, 'G': 157, 'B': 48}, '104': {'R': 50, 'G': 148, 'B': 45}, '105': {'R': 63, 'G': 154, 'B': 58}, '106': {'R': 58, 'G': 143, 'B': 52}, '107': {'R': 70, 'G': 148, 'B': 64}, '108': {'R': 68, 'G': 139, 'B': 61}, '109': {'R': 48, 'G': 111, 'B': 40}, '110': {'R': 48, 'G': 107, 'B': 39}, '111': {'R': 48, 'G': 102, 'B': 40}, '112': {'R': 57, 'G': 108, 'B': 51}, '113': {'R': 62, 'G': 110, 'B': 58}, '114': {'R': 59, 'G': 105, 'B': 59}, '115': {'R': 61, 'G': 99, 'B': 86}, '116': {'R': 123, 'G': 147, 'B': 195}, '117': {'R': 125, 'G': 140, 'B': 223}, '118': {'R': 124, 'G': 133, 'B': 226}, '119': {'R': 129, 'G': 135, 'B': 233}, '120': {'R': 130, 'G': 132, 'B': 232}, '121': {'R': 135, 'G': 135, 'B': 233}, '122': {'R': 114, 'G': 113, 'B': 207}, '123': {'R': 117, 'G': 113, 'B': 207}, '124': {'R': 121, 'G': 117, 'B': 212}, '125': {'R': 115, 'G': 112, 'B': 203}, '126': {'R': 123, 'G': 121, 'B': 204}, '127': {'R': 120, 'G': 119, 'B': 199}, '128': {'R': 125, 'G': 123, 'B': 207}, '129': {'R': 107, 'G': 104, 'B': 191}, '130': {'R': 101, 'G': 98, 'B': 185}, '131': {'R': 104, 'G': 101, 'B': 188}, '132': {'R': 104, 'G': 102, 'B': 186}, '133': {'R': 107, 'G': 106, 'B': 186}, '134': {'R': 102, 'G': 102, 'B': 176}, '135': {'R': 83, 'G': 84, 'B': 151}, '136': {'R': 91, 'G': 93, 'B': 154}, '137': {'R': 83, 'G': 86, 'B': 141}, '138': {'R': 85, 'G': 88, 'B': 141}, '139': {'R': 79, 
    'G': 82, 'B': 133}, '140': {'R': 83, 'G': 86, 'B': 139}, '141': {'R': 80, 'G': 83, 'B': 138}, '142': {'R': 55, 'G': 57, 'B': 114}, '143': {'R': 52, 'G': 52, 'B': 112}, '144': {'R': 57, 'G': 55, 'B': 118}, '145': {'R': 57, 'G': 55, 'B': 118}, '146': {'R': 57, 'G': 58, 'B': 115}, '147': {'R': 52, 'G': 58, 'B': 110}, '148': {'R': 49, 'G': 57, 'B': 104}, '149': {'R': 48, 'G': 55, 'B': 97}, '150': {'R': 50, 'G': 55, 'B': 93}, '151': {'R': 56, 'G': 54, 'B': 93}, '152': {'R': 55, 'G': 43, 'B': 83}, '153': {'R': 65, 'G': 39, 'B': 84}, '154': {'R': 74, 'G': 31, 'B': 85}, '155': {'R': 77, 'G': 19, 'B': 80}, '156': {'R': 82, 'G': 9, 'B': 80}, '157': {'R': 92, 'G': 5, 'B': 84}, '158': {'R': 99, 'G': 3, 'B': 90}, '159': {'R': 92, 'G': 6, 'B': 79}, '160': {'R': 73, 'G': 17, 'B': 56}, '161': {'R': 30, 'G': 0, 'B': 15}, '162': {'R': 23, 'G': 0, 'B': 11}, '163': {'R': 14, 'G': 0, 'B': 9}, '164': {'R': 5, 'G': 0, 'B': 5}, '165': {'R': 2, 'G': 2, 'B': 4}, '166': {'R': 3, 'G': 3, 'B': 3}, '167': {'R': 0, 'G': 0, 'B': 0}, '168': {'R': 1, 'G': 1, 'B': 0}}
    
    mincur = -1
    lvl = None

    for level in mined:
        c1 = { "R": rgb[0], "G": rgb[1], "B": rgb[2] }
        c2 = { "R": mined[level]["R"], "G" : mined[level]["G"], "B": mined[level]["B"] }
        Δc = RedMeanEuclidean(c1, c2)
        if mincur == -1 or Δc < mincur:
            mincur = Δc
            lvl = int(level)
    print(lvl)
    concentration = round((168-lvl)/64, 1)
    if concentration > 1:
        print(lvl, concentration)
    return concentration

def process_scan(tracer):
    Scans = []
    da = []
    for cropped_scan in os.listdir("./Client/" + tracer + "/Scans"):
        Scans.append(cv2.imread("./Client/" + tracer + "/Scans/" + cropped_scan))
    i=0
    for Scan in Scans:
        print(i)
        i+=1
        H, W, Channels = Scan.shape
        for x in range(H):
            print(x)
            for y in range(W):
                rgb = [Scan[x, y, 2], Scan[x, y, 1], Scan[x, y, 0]]
                concentration = RGB_to_Concentration(rgb)
                if concentration != 0.0:
                    da.append(concentration)
# print(process_scan('AV45'))
# print(RGB_to_Concentration([255, 0, 0]))
produce_scans_OASIS3()
print("--- %s seconds ---" % (time.time() - start_time))