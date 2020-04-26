import os
import numpy as np
from absl import app


def main(argv):
    #get the csv
    csvArr = np.genfromtxt('../vott-csv-export/Ant_05_tags-export.csv', dtype='<U42', delimiter=',', comments=None)
    print(csvArr)
    #delete label
    csvArr = np.delete(csvArr, 5, 1)
    csvArr = np.delete(csvArr, 0, 0)

    #shuffle and rename columns
    csvArr[:,[0, 4]] = csvArr[:,[4, 0]]

    numRow = np.size(csvArr, 0)
    i=0
    print(csvArr)
    #rename images and files
    while i < numRow:
        curName = csvArr[i][4]
        curName = curName.replace("\"","")
        print("line "+str(i)+". Name: "+curName)
        #change name of image
        newName = str(i)+'.jpg'
        csvArr[i][4] = newName
        #change corresponding name of image
        os.rename('photos/'+curName, 'photos/'+newName)
        i = i+1
    np.savetxt("data.csv", csvArr, delimiter=",", fmt='%s')

if __name__ == "__main__":
    app.run(main)