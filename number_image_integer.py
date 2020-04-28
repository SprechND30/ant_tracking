import os
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('directory', None, 'Directory holding the files.')

# Remember NOT to include a leading or trailing '/' for the directory name!!
def main(argv):
  directory = os.fsencode(FLAGS.directory)
  i = 0
  for file in os.listdir(directory):
      filename = os.fsdecode(file)  
      os.rename(FLAGS.directory+'/'+filename, FLAGS.directory+'/'+i+".jpg")
      

if __name__ == "__main__":
    app.run(main)