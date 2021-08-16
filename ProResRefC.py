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

headers = ["filename", "start", "end", "signal end", "clean duration", "noisy duration", "clean percentage", "noisy percentage"]
directory = "./mitdbannotationsfile"
with open('./ReqOutput2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow((headers))
    totalclean = 0
    totalnoisy = 0
    totalcount = 0
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            anno = pd.read_csv(directory+"/"+filename, sep="\t")
            writer.writerow([filename])
            clean = ""
            noisy = ""
            cleancount = 0
            noisycount = 0
            flagn = 0
            flagc = 0
            for index, row in anno.iterrows():
                if row["Type"] == '~':
                    if flagc == 1:
                        writer.writerow([filename, samplec, row["Sample"], " ", " ", " ", " ", " "])
                        cleancount += row["Sample"] - samplec
                        flagc = 0
                    if flagn == 0:
                        startn = row["Time"]
                        samplen = row["Sample"]
                        i = index
                        flagn = 1
                    else:
                        noisycount += row["Sample"] - samplen           
                        flagn = 0
                elif flagn == 0:
                    if flagc == 0:
                        samplec = row["Sample"]
                        flagc = 1
            writer.writerow([filename, samplec, row["Sample"], " ", " ", " ", " ", " "])
            cleancount += row["Sample"] - samplec
            data = [filename, " ", " ", row["Sample"]]
            data.append(toTime(cleancount))
            data.append(toTime(noisycount))
            data.append(round(100*cleancount/(cleancount+noisycount), 2))
            data.append(round(100*noisycount/(cleancount+noisycount), 2))
            writer.writerow(data)
            totalclean += cleancount
            totalnoisy += noisycount
            totalcount += row["Sample"]
    cleanpercent = "{:.2f}".format(round(100*totalclean/(totalclean+totalnoisy), 2))
    noisypercent = "{:.2f}".format(round(100*totalnoisy/(totalclean+totalnoisy), 2))
    #totalclean = toTime(totalclean)
    #totalnoisy = toTime(totalnoisy)
    writer.writerow(["total", " ", " ", totalcount, totalclean, totalnoisy, cleanpercent, noisypercent])
print("Total Clean Duration:", totalclean)
print("Total Noisy Duration:", totalnoisy)
print("Percentage of Overall Time that is Clean:", cleanpercent+"%")
print("Percentage of Overall Time that is Noisy:", noisypercent+"%")