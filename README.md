# TrackYourData

This repository contains the code elements of the Bachelor thesis "Track Your Data! Semantic Searchover Logs"

It consists of three main components:
server_audit.log (MariaDB Audit Plugin logfile)
log-to.csv.py (raw log to csv convertor)
log-analysis.py (csv to rdf convertor)


Prerequisits:
-Installation of Python 3
-Programming environment (recommendation: JetBrains PyCharm https://www.jetbrains.com/pycharm/download/)

Importation of the project:
-Extract TrackYourData.zip
-Open PyCharm
-Click on open
-Select the folder where TrackYourData.zip has been extracted to

IMPORTANT
How to use the scripts:
-A sample log of the MariaDB Audit Plugin is already included
-Execute log-to-csv.py via right-click on it and clicking 'run'. A file 'server_audit.csv' will be created.
-Execute log-analysis.py via right-click on it clicking 'run'. A file 'log.rdf' will be created. The console will also print out the contents of the file.




