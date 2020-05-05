import os
from absl import app
from absl import flags
from bisect import bisect_left

FLAGS = flags.FLAGS

flags.DEFINE_string('original_directory', None, 'Directory holding the files.')
flags.DEFINE_string('destination_directory', None, 'Directory holding the files.')

# Remember NOT to include a leading or trailing '/' for the directory name!!
def main(argv):
  directory = os.fsencode(FLAGS.original_directory)

  floatNames = []

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    fileFloat = getFloat(filename)
    if(fileFloat!=None):
      floatNames.append(fileFloat)
  floatNames.sort()
  #print(floatNames)
  i = 0
  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    newFilename = str(BinSearch(floatNames, getFloat(filename))) + '.jpg'
    print(filename + ' --> '+newFilename)
    os.rename(FLAGS.original_directory+'/'+filename, FLAGS.destination_directory+'/'+newFilename)
    i += 1
      

def getFloat(filename):
  splitAroundTime = filename.split("t=")
  if(len(splitAroundTime) > 1):
    return float(splitAroundTime[1].split(".j")[0])
  else:
    return None

  
def BinSearch(a, x):
   i = bisect_left(a, x)
   if i != len(a) and a[i] == x:
      return i
   else:
      return -1
  

if __name__ == "__main__":
    app.run(main)