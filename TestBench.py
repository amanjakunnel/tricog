import pandas as pd
import os

#Framework to to find true/false positives/negatives
directory = "./mitdbannotationsfile"
totaltp = 0
totaltn = 0
totalfp = 0
totalfn = 0
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt"):
        anno = pd.read_csv(directory+"/"+filename, sep="\t")
        trueposcount = 0
        truenegcount = 0
        falseposcount = 0
        falsenegcount = 0
        rlflagn = 0
        rlflagc = 0
        prflagn = 0
        prflagc = 0
        pred = " " * len(anno["Time"].tolist()) #placeholder for function/iterable through which j traverses for predicitons
        for (index, row), pr in zip(anno.iterrows(), pred):
            qualsign = row["Type"]
            if qualsign == '~':
                if rlflagc == 1:
                    rlflagc = 0
                if rlflagn == 0:
                    rlflagn = 1
                else:
                    rlflagn = 0
            elif rlflagn == 0:
                if rlflagc == 0:
                    rlflagc = 1
            if pr == '~':
                if prflagc == 1:
                    prflagc = 0
                if prflagn == 0:
                    prflagn = 1
                else:
                    prflagn = 0
            elif prflagn == 0:
                if prflagc == 0:
                    prflagc = 1
            if qualsign == pred == '~':
                if rlflagn == prflagn:
                    if rlflagn == 0:
                        trueposcount += 1
                    else:
                        truenegcount += 1
                else:
                    if prflagn == 0:
                        falsenegcount += 1
                    else: 
                        falseposcount += 1
            elif rlflagn == prflagn == 1:
                trueposcount += 1
            elif rlflagc == prflagc == 1:
                truenegcount += 1
            elif rlflagn == prflagc == 1:
                falsenegcount += 1
            elif rlflagc == prflagn == 1:
                falseposcount += 1
        total = trueposcount + truenegcount + falseposcount + falsenegcount
        truepos = trueposcount/total
        trueneg = truenegcount/total
        falsepos = falseposcount/total
        falseneg = falsenegcount/total
        '''print(filename)
        print("\tTrue Positives are", str(truepos*100)+"%")
        print("\tTrue Negatives are", str(trueneg*100)+"%")
        print("\tFalse Positives are", str(falsepos*100)+"%")
        print("\tFalse Negatives are", str(falseneg*100)+"%")'''
        totaltp += trueposcount
        totaltn += truenegcount
        totalfp += falseposcount
        totalfn += falsenegcount
total = totaltp + totaltn + totalfp + totalfn
print("Total True Positives are", "{:.2f}".format(totaltp*100/total)+"%")
print("Total True Negatives are", "{:.2f}".format(totaltn*100/total)+"%")
print("Total False Positives are", "{:.2f}".format(totalfp*100/total)+"%")
print("Total False Negatives are", "{:.2f}".format(totalfn*100/total)+"%")