from Process import process_scan_path
import time
import concurrent.futures
import os

start_time = time.time()

def get_tracers():
    tracers = []
    for tracer in os.listdir("../Client"):
        if "." not in tracer:
            tracers.append(tracer)
    return tracers 

def data_mine_tracer(tracer):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        ### Get a list of files to process
        scans = []
        for scan in os.listdir("../Client/" + tracer + "/Scans"): 
            scans.append("../Client/" + tracer + "/Scans/" + scan) 
        executor.map(process_scan_path, scans)

all_t = get_tracers()
print(all_t)
for tracer in all_t:
    data_mine_tracer(tracer)

print("--- %s seconds ---" % (time.time() - start_time))