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

cleanstart = ["cln start"]
cleanend = ["cln end"]
cleancum = ["cln cum"]
noisystart = ["ns start"]
noisyend = ["ns end"]
noisycum = ["ns cum"]
clnrstart = ["cln train start"]
clnrend = ["cln train end"]
clnrcum = ["cln train cum"]
nsrstart =["ns train start"]
nsrend = ["ns train end"]
nsrcum = ["ns train cum"]
clntstart = ["cln test start"]
clntend = ["cln test end"]
clntcum = ["cln test cum"]
nststart = ["ns test start"]
nstend = ["ns test end"]
nstcum = ["ns test cum"]
clnvstart = ["cln val start"]
clnvend = ["cln val end"]
clnvcum = ["cln val cum"]
nsvstart = ["ns val start"]
nsvend = ["ns val end"]
nsvcum = ["ns val cum"]


cleanset = pd.read_csv("DatasetC.csv")
noisyset = pd.read_csv("Dataset.csv")
headers = ["file", "clean intervals", "cumulative", "noisy intervals", "cumulative", "clean training", "cumulative", "noisy training", "cumulative", "clean testing", "cumulative", "noisy testing", "cumulative", "clean validation", "cumulative", "noisy validation", "cumulative"]
directory = "./mitdbannotationsfile"
totalclean = 0
totalnoisy = 0
filenames = ["filenames"]
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt"):
        clncount = 0
        nscount = 0
        clnrcount = 0
        nsrcount = 0
        clntcount = 0
        nstcount = 0
        clnvcount = 0
        nsvcount = 0
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
                    cleanstart.append(samplec)
                    cleanend.append(row["Sample"])
                    clncount += 1
                    cleancount += row["Sample"] - samplec
                    flagc = 0
                if flagn == 0:
                    startn = row["Time"]
                    samplen = row["Sample"]
                    flagn = 1
                else:
                    noisystart.append(samplen)
                    noisyend.append(row["Sample"])
                    nscount += 1
                    noisycount += row["Sample"] - samplen
                    flagn = 0
            elif flagn == 0:
                if flagc == 0:
                    startc = row["Time"]
                    samplec = row["Sample"]
                    flagc = 1
        cleanstart.append(samplec)
        cleanend.append(row["Sample"])
        clncount += 1
        cleancount += row["Sample"] - samplec
        crc = 0
        ctc = 0
        cvc = 0
        nrc = 0
        ntc = 0
        nvc = 0
        fileclean = cleanset[cleanset["filename"]==filename]
        for idx, r in fileclean.iterrows():
            if r["set type"] == "Training":
                clnrstart.append(r["start"])
                clnrend.append(r["end"])
                clnrcount += 1
                crc += r["end"] - r["start"]
            if r["set type"] == "Test":
                clntstart.append(r["start"])
                clntend.append(r["end"])
                clntcount += 1
                ctc += r["end"] - r["start"]
            if r["set type"] == "Validation":
                clnvstart.append(r["start"])
                clnvend.append(r["end"])
                clnvcount += 1
                cvc += r["end"] - r["start"]
        filenoisy = noisyset[noisyset["filename"]==filename]
        for idx, r in filenoisy.iterrows():
            if r["set type"] == "Training":
                nsrstart.append(r["start"])
                nsrend.append(r["end"])
                nsrcount += 1
                nrc += r["end"] - r["start"]
            if r["set type"] == "Test":
                nststart.append(r["start"])
                nstend.append(r["end"])
                nstcount += 1
                ntc += r["end"] - r["start"]
            if r["set type"] == "Validation":
                nsvstart.append(r["start"])
                nsvend.append(r["end"])
                nsvcount += 1
                nvc += r["end"] - r["start"]
        '''crc = toTime(crc)
        ctc = toTime(ctc)
        cvc = toTime(cvc)
        nrc = toTime(nrc)
        ntc = toTime(ntc)
        nvc = toTime(nvc)'''
        '''data.append(round(100*cleancount/(cleancount+noisycount), 2))
        data.append(round(100*noisycount/(cleancount+noisycount), 2))'''
        totalclean += cleancount
        totalnoisy += noisycount
        filecount = max(clncount, nscount, clnrcount, clntcount, clnvcount, nsrcount, nstcount, nsvcount)
        filenames += [filename] * filecount
        cleancount = cleancount
        noisycount = noisycount
        cleancum += [cleancount] * filecount
        noisycum += [noisycount] * filecount
        clnrcum += [crc] * filecount
        nsrcum += [nrc] * filecount
        clntcum += [ctc] * filecount
        nstcum += [ntc] * filecount
        clnvcum += [cvc] * filecount
        nsvcum += [nvc] * filecount
        cleanstart += [" "] * (filecount - clncount)
        cleanend += [" "] * (filecount - clncount)
        noisystart += [" "] * (filecount - nscount)
        noisyend += [" "] * (filecount - nscount)
        clnrstart += [" "] * (filecount - clnrcount)
        clnrend += [" "] * (filecount - clnrcount)
        clntstart += [" "] * (filecount - clntcount)
        clntend += [" "] * (filecount - clntcount)
        clnvstart += [" "] * (filecount - clnvcount)
        clnvend += [" "] * (filecount - clnvcount)
        nsrstart += [" "] * (filecount - nsrcount)
        nsrend += [" "] * (filecount - nsrcount)
        nststart += [" "] * (filecount - nstcount)
        nstend += [" "] * (filecount - nstcount)
        nsvstart += [" "] * (filecount - nsvcount)
        nsvend += [" "] * (filecount - nsvcount)
ddff = pd.DataFrame(list(zip(filenames, cleanstart, cleanend, cleancum, noisystart, noisyend, noisycum, clnrstart, clnrend, clnrcum, nsrstart, nsrend, nsrcum, clntstart, clntend, clntcum, nststart, nstend, nstcum, clnvstart, clnvend, clnvcum, nsvstart, nsvend, nsvcum)))
ddff.to_csv("ColmOutput.csv")
exit()
cleanpercent = "{:.2f}".format(round(100*totalclean/(totalclean+totalnoisy), 2))
noisypercent = "{:.2f}".format(round(100*totalnoisy/(totalclean+totalnoisy), 2))
totalclean = toTime(totalclean)
totalnoisy = toTime(totalnoisy)
#writer.writerow(["total", "N/A", "N/A", totalclean, totalnoisy, cleanpercent, noisypercent])
print("Total Clean Duration:", totalclean)
print("Total Noisy Duration:", totalnoisy)
print("Percentage of Overall Time that is Clean:", cleanpercent+"%")
print("Percentage of Overall Time that is Noisy:", noisypercent+"%")