#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Contains data from the Monash Unviersity Woodside Living Lab Building 
recording of the 22 Sept 2021 Mansfield 5.8M earthquake

Basic data reading and plotting
"""

# pip install npTDMS for reading the NI TDMS file type
from nptdms import TdmsFile
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Reading the NI TDMS file
tdms_file = TdmsFile.read("202109220920_SHM-6.tdms")
channels = tdms_file.groups()[0].channels()

# Quick plot of the data
fig, ax = plt.subplots()
for c in channels:
    data = c[:]
    t = c.time_track(absolute_time=True)
    ax.plot(t, data, label=c.name)

ax.legend()
plt.show()

# Sample rate and start time in UTC
t0 = channels[0].properties["wf_start_time"]
fs = 1 / channels[0].properties["wf_increment"]
print(f"Record start time {t0}")
print(f"Sample rate: {fs}")

# Export relevant data window to CSV (~81 MB file)
c0 = channels[0]

t0 = c0.properties["wf_start_time"]
ts = t0 + np.timedelta64(60, "s")
tf = t0 + np.timedelta64(6, "m")

t = c0.time_track(absolute_time=True)
idx = np.where((t > ts) & (t < tf))
tw = t[idx]

df = pd.DataFrame()
df["t"] = tw

for c in channels:
    zero_data = c[: (t < ts).sum()]
    data = c[idx] - zero_data.mean()
    df[c.name] = data

df.to_csv("accels.csv", index=False)
