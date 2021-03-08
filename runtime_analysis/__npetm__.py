import neuropetm
import concurrent.futures
import os
import time
import sys

# Data mining all tracers in ./Client to produce a multimodal 3d PET Scan viewable on Plotly
def data_mine_client(client):
    for tracer in os.listdir("./tests/" + client + "/"):
        if "." in tracer: continue
        scans = []
        for scan in os.listdir("./tests/" + client + "/" + tracer + "/Scans"):
            scans.append("./tests/" + client + "/" + tracer + "/Scans/" + scan)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(neuropetm.process_scan_path, scans)

def PRODUCE_NEUROPETM_SCAN(client):
    start_time = time.time()
    print("---------------------")

    produce_scans = time.time()
    neuropetm.produce_scans_OASIS3(client)
    print("PRODUCE SCANS TIME", client, ("--- %s seconds ---" % (time.time() - produce_scans)))

    data_mine = time.time()
    data_mine_client(client)
    print("DATA MINE TIME", client, ("--- %s seconds ---" % (time.time() - data_mine)))

    produce_mm_scan = time.time()
    neuropetm.produce_multimodal_scan(client)
    print("PRODUCE MM SCAN TIME", client, ("--- %s seconds ---" % (time.time() - produce_mm_scan)))

    print("TOTAL TIME", client, ("--- %s seconds ---" % (time.time() - start_time)))
    print("---------------------")

for client in os.listdir("./tests/"):
    # for testcase in range(1, 6):
    PRODUCE_NEUROPETM_SCAN(client)