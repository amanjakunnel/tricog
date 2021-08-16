import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

headers = ["filename", "start", "end", "set type"]
with open('./Dataset.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow((headers))
    file = pd.read_csv("ReqOutput.csv")
    file["start"].replace(' ', np.nan, inplace=True)
    df = file[["filename", "start", "end"]].dropna()
    count = 0
    while count < 2618691*0.6:
        rand = df.sample()
        count += int(rand["end"]) - int(rand["start"])
        row = rand.values[0].tolist()
        row.append("Training")
        writer.writerow(row)
        df = df.drop(rand.index)
    count = 0
    while count < 2618691*0.2:
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