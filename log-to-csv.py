import csv

filein = "server_audit.log"
fileout = "server_audit.csv"
with open(filein, "r") as file:
        with open(fileout, "w") as fileout:
            for line in file:
                rep1 = line.replace(",",  ";", 8)
                rep2 = rep1.replace("\\'", "")
                rep3 = rep2.replace('\',', "\';")

                # replace e.g. disconnect comma
                rep4 = rep3.replace(';,', ";;")

                # replace blank space between date and time
                rep5 = rep4.replace(" ", ";", 1)

                fileout.write(rep5)
print("Logfile " + str(filein) + " has been converted to CSV: " + str(fileout.name))
