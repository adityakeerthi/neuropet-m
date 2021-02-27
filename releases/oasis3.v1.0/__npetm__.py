import neuropetm
import concurrent.futures
import datetime
import os
import time
import sys

start_time = time.time()

# Data mining all tracers in ./Client to produce a multimodal 3d PET Scan viewable on Plotly
def data_mine_client():
    for tracer in os.listdir("./Client"):
        if "." in tracer: continue
        scans = []
        for scan in os.listdir("./Client/" + tracer + "/Scans"):
            scans.append("./Client/" + tracer + "/Scans/" + scan)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(neuropetm.process_scan_path, scans)

def SETUP():
    neuropetm.setup_environment()
    print("\n**NEXT STEPS** Please insert the PET Scans from the OASIS-3 Dataset to proceed further with the analysis.")

def EDIT_THRESHOLD():
    neuropetm.edit_threshold()

def PRODUCE_NEUROPETM_SCAN():
    print("\nPROCESSING...")
    neuropetm.produce_scans_OASIS3()
    data_mine_client()
    neuropetm.produce_multimodal_scan()
    print("Complete\n")

MESSAGE = "1. Setup environment. \n2. Edit file name AND threshold values for PET Scans. \n3. Produce NeuroPET-M Scan. \n4. Abort program. \n"

def init():
    while True:
        print("\n" + MESSAGE)
        choice = int(input("Please enter a number that corresponds to the following choices above: "))

        if choice == 1: SETUP()
        elif choice == 2: EDIT_THRESHOLD()
        elif choice == 3: PRODUCE_NEUROPETM_SCAN()
        elif choice == 4: sys.exit()
        else: 
            print("Program aborted. Invalid Input.")
            sys.exit()

init()

print("--- %s seconds ---" % (time.time() - start_time))