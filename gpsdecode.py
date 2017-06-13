import csv
import gmplot
import sys


from time import strftime

def convertfunction (value):
    degVal = value/100
    degrees = int(degVal)
    decMinutesSeconds = (value-float(float(degrees)*100.0)) / 60.0
    return degrees+decMinutesSeconds

final_list_gps= []
final_list_data= []
final_lat= []
final_long= []
final_alt = []
time_stamp= []
final_time= []

filename_gps = str(sys.argv[1])
filename_data = str(sys.argv[2])

with open(filename_gps,'rU')as csvfile:
    initial_list = csv.reader(csvfile,delimiter =',',quotechar = '|')
    for row in initial_list:
        if len(row)>0and row[0] != '' and len(row)>3 and len(row)> 11 and row[1] == 'GPGGA' and row[4]== 'N' and row[11]=='M':
            final_list_gps.append(row)


with open('GPS_Cleaned.csv','w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in final_list_gps:
        spamwriter.writerow(row)


with open('GPS_coordinates.csv','w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in final_list_gps:
        try:
            float(row[3])
            float(row[5])
            float(row[10])
        except:
            continue
        if float(row[3])>3000.0 and float(row[3])<4000.0 and float(row[5])>(8000) and float(row[5]) < (9000):
            row[3]= str(convertfunction(float(row[3])))
            row[5]= str((-1)*convertfunction(float(row[5])))
            row[10] = str(convertfunction(float(row[10])))
            final_lat.append(float(row[3]))
            final_long.append(float(row[5]))
            final_alt.append(float(row[10]))
            final_time.append(float(row[2]))
            time_stamp.append(row[0])
            spamwriter.writerow([row[3],row[5],row[10]])


gmap = gmplot.GoogleMapPlotter(final_list_gps[1][3], final_list_gps[1][5], 12)

gmap.marker(final_lat[1],final_long[1],title="START")
gmap.marker(final_lat[len(final_lat)-1],final_long[len(final_long)-1],title ="END")
gmap.plot(final_lat,final_long, 'r',edge_width = 5)


gmap.draw("GPS_Map.html")



with open(filename_data,'rU')as csvfile:
    initial_list = csv.reader(csvfile,delimiter =',',quotechar = '|')
    csvfile.next()
    for row in initial_list:
        if (row[10] in time_stamp):
            final_list_data.append(row)

gmap2 = gmplot.GoogleMapPlotter(final_list_gps[1][3], final_list_gps[1][5], 12)

gmap2.marker(final_lat[1],final_long[1],title="START")
gmap2.marker(final_lat[len(final_lat)-1],final_long[len(final_long)-1],title ="END")
gmap2.plot(final_lat,final_long, 'r',edge_width = 5)

steps = len(final_lat)/30

for i in range(0,len(final_lat),steps):
    pre = strftime("%Y-%m-%d ")  # "2007-04-15T"
    hour = str(int(final_list_gps[i][2][:2]) -5)
    minute = final_list_gps[i][2][2:4]
    second = final_list_gps[i][2][4:6]
    curtime = pre + hour + ":" + minute + ":" + second
    gmap2.marker(final_lat[i], final_long[i], title = "Time: "+ curtime + " Temp: "+str(final_list_data[i][0])+"C Alt: "+str(final_list_data[i][2]))



gmap2.draw("GPS_Map_with_data.html")

with open('Data_combined.csv','w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0,len(final_lat)-1):
        final_list_data[i].append(final_lat[i])
        final_list_data[i].append(final_long[i])
        final_list_data[i].append(final_time[i])
        spamwriter.writerow(final_list_data[i])