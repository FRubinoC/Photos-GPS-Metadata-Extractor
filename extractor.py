from PIL import Image
#from simplekml import Kml
from PIL.ExifTags import TAGS, GPSTAGS
import os

path = "" #Replace the value of this variable with the path of the folder where you want to save the kvm file.

def printInfoImages(path, Filename):
    #print("Current working directory: {0}".format(os.getcwd()))
    cwd = os.chdir(path)
    #print("Current working directory: {0}".format(os.getcwd()))
    for f in os.listdir('.'):
        if f.endswith('.jpg'):
            print(f)
            
            image = Image.open(f)
            exifdata = image._getexif()
            if exifdata:
                gpsinfo = {}
                for tag, value in exifdata.items():
                    #print(tag)
                    decoded = TAGS.get(tag, tag)
                    #print(decoded)
                    if decoded == 'GPSInfo':
                        
                        for key in exifdata[tag].keys():
                            decode = GPSTAGS.get(key,key)
                            gpsinfo[decode] = exifdata[tag][key]
                        #exif_gps_table[decoded] = value
                        #print(exif_gps_table[decoded])
                print (gpsinfo)
                saveInKml(gpsinfo, Filename)
                #print(exifdata)
            print('\n')
    for d in os.listdir():
        if os.path.isdir(d):
            printInfoImages(d, Filename)
            cwd = os.chdir('..')




def saveInKml(gpsinfo, Filename):
        tuplat = gpsinfo["GPSLatitude"]
        lat = float(tuplat[0]) + float(tuplat[1])/60 + float(tuplat[2])/3600
        tuplon = gpsinfo["GPSLongitude"]
        lon = float(tuplon[0]) + float(tuplon[1])/60 + float(tuplon[2])/3600
        alt = gpsinfo["GPSAltitude"]

        latref = gpsinfo["GPSLatitudeRef"]
        if latref == "S":
            lat = -lat

        longref = gpsinfo["GPSLongitudeRef"]
        if longref == "W":
            lon = -lon
        
        file = open(path+Filename+".kml", "a")
        file.write("<Placemark> <name>Simple placemark</name>\n <description> Gps Placemark from Image </description>  <Point>")
        file.write("<coordinates>"+str(lon)+","+str(lat)+","+str(alt)+"</coordinates>")
        file.write("</Point> </Placemark>\n")
        
    
    
      

                
def trackingGPSfromJPG():
    Filename = input("Insert the name of the file that you want to use to save the GPS info.")
    file = open(path+Filename+".kml", "a")
    file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n")
    file.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n<Document>\n")
    file.close()
    printInfoImages('D:/', Filename)
    file = open(path+Filename+".kml", "a")
    file.write("</Document>\n</kml>\n")
    file.close()

trackingGPSfromJPG()



