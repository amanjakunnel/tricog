import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import random

fil = []
headers = ["filename", "start", "end", "set type"]
directory = "./mitdbannotationsfile"
for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            fil.append(filename)
with open('./DatasetC.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow((headers))
    file = pd.read_csv("ReqOutput2.csv")
    file["start"].replace(' ', np.nan, inplace=True)
    df = file[["filename", "start", "end"]].dropna()
    count = 0
    while count < 26155580*0.1:
        ff = random.sample(fil, 1)
        fff = ff[0]
        samdf = df[df["filename"] == fff]
        flag = 0
        for idx, r in samdf.iterrows():
            count += int(r["end"]) - int(r["start"])
            row = r.values.tolist()
            row.append("Test")
            writer.writerow(row)
            df = df[df["filename"] != fff]
            if count > 26155580*0.1:
                flag = 1
                break
        if flag == 1:
            break
    count = 0
    while count < 26155580*0.1:
        ff = random.sample(fil, 1)
        fff = ff[0]
        samdf = df[df["filename"] == fff]
        flag = 0
        for idx, r in samdf.iterrows():
            count += int(r["end"]) - int(r["start"])
            row = r.values.tolist()
            row.append("Validation")
            writer.writerow(row)
            df = df[df.filename != fff]
            if count > 26155580*0.1:
                flag = 1
                break
        if flag == 1:
            break
    while count < 26155580*0.6:
        rand = df.sample()
        count += int(rand["end"]) - int(rand["start"])
        row = rand.values[0].tolist()
        row.append("Training")
        writer.writerow(row)
        df = df.drop(rand.index)
    count = 0
    while count < 26155580*0.1:
        rand = df.sample()
        count += int(rand["end"]) - int(rand["start"])
        row = rand.values[0].tolist()
        row.append("Test")
        writer.writerow(row)
        df = df.drop(rand.index)
    while len(df.index) > 0:
        rand = df.sample()
        row = rand.values[0].tolist()
        row.append("Validation")
        writer.writerow(row)
        df = df.drop(rand.index)