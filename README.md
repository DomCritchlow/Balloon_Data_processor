This program will produce cleaned up GPS and data files. 
It also produces two html files with a map of the gps locations. 
Hovering over a marker will show the annotation. 


In order to run type:

python gpsdecode.py GPSDATA.TXT WORK.CSV

 
GPSDATA.TXT is a csv file with the first column being a random number for matching, and the from there on out GPGGA GPS string. 

WORK.CSV is a csv file we use to store data from our other sensors. temperature and so on.


![Screenshot image] (Screenshot.png)
