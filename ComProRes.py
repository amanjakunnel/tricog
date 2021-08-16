import pandas as pd
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

cleanset = pd.read_csv("DatasetC.csv")
noisyset = pd.read_csv("Dataset.csv")
headers = ["file", "clean intervals", "cumulative", "noisy intervals", "cumulative", "clean training", "cumulative", "noisy training", "cumulative", "clean testing", "cumulative", "noisy testing", "cumulative", "clean validation", "cumulative", "noisy validation", "cumulative"]
directory = "./mitdbannotationsfile"
with open('./CompOutput.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow((headers))
    totalclean = 0
    totalnoisy = 0
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            anno = pd.read_csv(directory+"/"+filename, sep="\t")
            data = [filename]
            clean = ""
            noisy = ""
            cleancount = 0
            noisycount = 0
            flagn = 0
            flagc = 0
            for index, row in anno.iterrows():
                if row["Type"] == '~':
                    if flagc == 1:
                        clean += "("+startc+"-"+row["Time"]+") "
                        cleancount += row["Sample"] - samplec
                        flagc = 0
                    if flagn == 0:
                        startn = row["Time"]
                        samplen = row["Sample"]
                        flagn = 1
                    else:
                        noisy += "("+startn+"-"+row["Time"]+") "
                        noisycount += row["Sample"] - samplen
                        flagn = 0
                elif flagn == 0:
                    if flagc == 0:
                        startc = row["Time"]
                        samplec = row["Sample"]
                        flagc = 1
            clean += "("+startc+"-"+row["Time"]+") "
            cleancount += row["Sample"] - samplec
            data.append(clean)
            data.append(toTime(cleancount))
            data.append(noisy)
            data.append(toTime(noisycount))
            clnr = ""
            clnt = ""
            clnv = ""
            nsr = ""
            nst = ""
            nsv = ""
            crc = 0
            ctc = 0
            cvc = 0
            nrc = 0
            ntc = 0
            nvc = 0
            fileclean = cleanset[cleanset["filename"]==filename]
            for idx, r in fileclean.iterrows():
                if r["set type"] == "Training":
                    clnr += "("+toTime(r["start"])+"-"+toTime(r["end"])+") "
                    crc += r["end"] - r["start"]
                if r["set type"] == "Test":
                    clnt += "("+toTime(r["start"])+"-"+toTime(r["end"])+") "
                    ctc += r["end"] - r["start"]
                if r["set type"] == "Validation":
                    clnv += "("+toTime(r["start"])+"-"+toTime(r["end"])+") "
                    cvc += r["end"] - r["start"]
            filenoisy = noisyset[noisyset["filename"]==filename]
            for idx, r in filenoisy.iterrows():
                if r["set type"] == "Training":
                    nsr += "("+toTime(r["start"])+"-"+toTime(r["end"])+") "
                    nrc += r["end"] - r["start"]
                if r["set type"] == "Test":
                    nst += "("+toTime(r["start"])+"-"+toTime(r["end"])+") "
                    ntc += r["end"] - r["start"]
                if r["set type"] == "Validation":
                    nsv += "("+toTime(r["start"])+"-"+toTime(r["end"])+") "
                    nvc += r["end"] - r["start"]
            crc = toTime(crc)
            ctc = toTime(ctc)
            cvc = toTime(cvc)
            nrc = toTime(nrc)
            ntc = toTime(ntc)
            nvc = toTime(nvc)
            data += [clnr, crc, clnt, ctc, clnv, cvc, nsr, nrc, nst, ntc, nsv, nvc]
            '''data.append(round(100*cleancount/(cleancount+noisycount), 2))
            data.append(round(100*noisycount/(cleancount+noisycount), 2))'''
            writer.writerow(data)
            totalclean += cleancount
            totalnoisy += noisycount
    cleanpercent = "{:.2f}".format(round(100*totalclean/(totalclean+totalnoisy), 2))
    noisypercent = "{:.2f}".format(round(100*totalnoisy/(totalclean+totalnoisy), 2))
    totalclean = toTime(totalclean)
    totalnoisy = toTime(totalnoisy)
    #writer.writerow(["total", "N/A", "N/A", totalclean, totalnoisy, cleanpercent, noisypercent])
print("Total Clean Duration:", totalclean)
print("Total Noisy Duration:", totalnoisy)
print("Percentage of Overall Time that is Clean:", cleanpercent+"%")
print("Percentage of Overall Time that is Noisy:", noisypercent+"%")