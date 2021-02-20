from neuropetm import process_scan_path, generate_pdset
import concurrent.futures
import plotly.express as px
import datetime
import os

# Using multiprocessing to mine each radioactive tracer PET Scan concurrently
def data_mine_tracer(tracer):
    scans = []
    for scan in os.listdir("./Client/" + tracer + "/Scans"):
        scans.append("./Client/" + tracer + "/Scans/" + scan)
    print(scans, tracer)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_scan_path, scans)

def generate_scan(tracer):
    dataframe = generate_pdset(tracer)
    fig = px.scatter_3d(dataframe, x='x', y='y', z='z', color='c', symbol='tracer')
    scan_name = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    fig.write_html("./" + scan_name + ".html")

generate_scan("AV45")