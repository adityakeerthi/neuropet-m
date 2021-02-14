from Display import generate_dataset, generate_scan_dataset
import pandas as pd
import plotly.express as px
import os

def get_data_list(tracer):
    dlist = []
    for info in os.listdir("../Client/" + tracer + "/Data"):
        dlist.append("../Client/" + tracer + "/Data/" + info)
    return dlist

# dlist = get_data_list("AV45")

# dset = generate_scan_dataset(dlist[0])
dset1 = generate_dataset("PIB")
dset2 = generate_dataset("AV45")

tcers1 = ["PIB" for i in range(len(dset1[0]))]
tcers2 = ["AV45" for i in range(len(dset2[0]))]
data_dict1 = {"x": dset1[0], "y": dset1[1], "z": dset1[2], "c": dset1[3], "tracer": tcers1}
data_dict2 = {"x": dset2[0], "y": dset2[1], "z": dset2[2], "c": dset2[3], "tracer": tcers2}
data_frame1 = pd.DataFrame(data_dict1)
data_frame2 = pd.DataFrame(data_dict2)

print(data_frame1)

fig = px.scatter_3d(data_frame1, x='x', y='y', z='z',
                    color='c', symbol='tracer')
fig = px.scatter_3d(data_frame2, x='x', y='y', z='z',
                    color='c', symbol='tracer')
# fig.show()
fig.write_html("../Graph.html")