import os
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('directory', None, 'Directory holding the files.')

# Remember NOT to include a leading or trailing '/' for the directory name!!
def main(argv):
  directory = os.fsencode(FLAGS.directory)

  for file in os.listdir(directory):
      filename = os.fsdecode(file)
      if(len(filename.split("#t=")) > 1):
        time = filename.split("#t=")[1].split(".jpg")[0]
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
        
        newFilename = timeInt + '.' + timeDec + '.jpg'
        
        os.rename(FLAGS.directory+'/'+filename, FLAGS.directory+'/'+newFilename)
      


if __name__ == "__main__":
    app.run(main)