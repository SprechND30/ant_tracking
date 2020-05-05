import os
import numpy as np
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('input_csv', None, 'CSV from which to get data.')
flags.DEFINE_boolean('rename', False, 'Rename files in ascending order.')


def main(argv):
    #get the csv
    csvArr = np.genfromtxt(FLAGS.input_csv, dtype='<U42', delimiter=',', comments=None)
    #delete label
    csvArr = np.delete(csvArr, 5, 1)
    csvArr = np.delete(csvArr, 0, 0)

    #shuffle and rename columns
    i = 0
    while(i < 4):
        i = i + 1
        csvArr[:,[i-1, i]] = csvArr[:,[i, i-1]]

    #rename images and files
    if(FLAGS.rename):
        numRow = np.size(csvArr, 0)
        i=0
        while i < numRow:
            curName = csvArr[i][4]
            curName = curName.replace("\"","")
            print("line "+str(i)+". Name: "+curName)

            '''if(len(curName.split("#t=")) > 1):
                time = curName.split("#t=")[1].split(".jpg")[0]
                timeInt = time.split(".")[0]

                if(len(time.split(".")) > 1):
                    timeDec = time.split(".")[1]
                else:
                    timeDec = ''
                timeDiff = 6 - len(timeDec)
                if(timeDiff > 0):
                    while(timeDiff > 0):
                        timeDiff = timeDiff-1
                        timeDec = timeDec + '0'
                
                curName = timeInt + '.' + timeDec + '.jpg''''

            #change name of image
            newName = str(i)+'.jpg'
            csvArr[i][4] = newName
            #change corresponding name of image
            #os.rename('train/images/'+curName, 'train/images/'+newName)
            i = i+1
    
    np.savetxt("data.csv", csvArr, delimiter=",", fmt='%s')

if __name__ == "__main__":
    app.run(main)