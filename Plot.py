import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import isnan
import csv
import os

from math import floor

def toTime(n):
    n /= 360
    nmin = int(n//60)
    nsecf = n % 60
    nsec = floor(nsecf)
    nmil = round((nsecf - nsec) * 1000)
    if nsec < 10:
        sec = "0"+str(nsec)
    else:
        sec = str(nsec)
    if nmin < 60:
        return str(nmin)+":"+sec+"."+str(nmil)
    else:
        nhr = int(nmin//60)
        nmin = floor(nmin%60)
        if nmin < 10:
            min = "0"+str(nmin)
        else:
            min = str(nmin)
        return str(nhr)+":"+min+":"+sec+"."+str(nmil)

def plotfile(file):
    intervals = pd.read_csv("ReqOutput.csv")
    flag = 0
    for index, row in intervals.iterrows():
        if row["filename"] == file and flag == 0:
            flag = 1
            continue
        if flag == 1:
            print(row)
            flow = pd.read_csv("mitdb/"+file, sep="\t", header=None)
            time = []
            signal = []
            f = 0
            c = 1
            print(flow)
            for idx, r in flow.iterrows():
                if r[0] == row["start"]:
                    print(r[0])
                    f = 1
                if f == 1:
                    time.append(toTime(r[0]))
                    signal.append(r[1])
                if r[0] == row["end"]:
                    print(r[0])
                    break
            plt.plot(time, signal)
            plt.title(file+" noise interval "+str(c))
            #idx = np.round(np.linspace(0, len(time) - 1, 6)).astype(int).tolist()
            #stamps = [time[x] for x in idx]
            #plt.xticks(stamps)
            plt.xlabel("Time Stamp")
            plt.ylabel("Signal")
            plt.show()
            c += 1
            flag = 0

plotfile("101.txt")

'''c = 1
intervals = pd.read_csv("ReqOutput.csv")
for index, row in intervals.iterrows():
    if row["start"] != row["end"]:
        filename = row["filename"]
        file = pd.read_csv("mitdb/"+filename, sep="\t", header=None)
        time = []
        signal = []
        flag = 0
        file = pd.read_csv("mitdb/"+filename, sep="\t", header=None)
        for idx, r in file.iterrows():
            if r[0] == row["start"]:
                flag = 1
            if flag == 1:
                time.append(toTime(r[0]))
                signal.append(r[1])
            if r[0] == row["end"]:
                break
        plt.plot(time, signal)
        plt.title(filename+" noise interval "+str(c))
        idx = np.round(np.linspace(0, len(time) - 1, 6)).astype(int).tolist()
        #stamps = [time[x] for x in idx]
        #plt.xticks(stamps)
        plt.xlabel("Time Stamp")
        plt.ylabel("Signal")
        plt.show()
        c += 1
        if row["filename"] != filename:
            c = 1'''