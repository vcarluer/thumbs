import sys
import pyparams #https://github.com/jbrendel/pyparams
import os
import logging
from PIL import Image #https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
import glob

logging.basicConfig(level = logging.DEBUG)
BASE_STORAGE = "/var/local/thumbs"

logging.debug("Initializing pyparams")
CONF= pyparams.Conf(
        conf_file_parameter         = "configfile",
        default_conf_file_locations = ["/etc/thumbs"],
        default_env_prefix          = "THUMBS_",
        #default_allowèunset_values  = False,
        param_dict                  = {
            "configfile" : {
                "default"   : "thumbs.conf",
                "conffile"  : None,
                "cmd_line"  : None
            },
            "baseStorage" : {
                "default"   : "/var/local/thumbs",
                "cmd_line"  : ('b', 'baseStorage')
            },
            "filePath" : {
                "default"   : "",
                "conffile"  : None,
                "cmd_line"  : ('p', 'filePath')
                },
            "force" : {
                "default"   : False,
                "param_type": pyparams.PARAM_TYPE_BOOL,
                "cmd_line"  : ('f', 'force')
                },
            "size" : {
                "default"   : 128,
                "param_type": pyparams.PARAM_TYPE_INT,
                "cmd_line"  : ('s', 'size')
                }
            }
        )
logging.info("THUMBS")
logging.info("--------------------------------------------------------")
logging.info("Available parameters:")
logging.info(CONF.make_doc())
logging.info("--------------------------------------------------------")

CONF.acquire(sys.argv[1:])
BASE_STORAGE = CONF.get("baseStorage")

def main():
    if CONF.get("filePath"):
        filePath = CONF.get("filePath")
        if os.path.isdir(filePath):
            logging.debug("dir path mode: {}".format(filePath))
            thumb_dir(filePath)
        else:
            logging.debug("file path mode: {}".format(filePath))
            thumb_file(filePath)

def thumb_dir(dirPath):
    globPattern = dirPath + "/**/*.jpg"
    for infile in glob.glob(globPattern, recursive=True):
        thumb_file(infile)

def thumb_file(filePath):
    logging.info("Scanning file path: {}".format(filePath))
    if not os.path.isfile(filePath):
        logging.info("Not a file path")
        sys.exit(1)
    filename, extension = os.path.splitext(filePath)
    if not extension == ".jpg":
        logging.info("Bad file extension. Only jpg supported")
        sys.exit(1)
    logging.debug("Removing heading / to join path")
    refPath = filePath[1:]
    dirPath = os.path.dirname(refPath)
    targetPath = os.path.join(BASE_STORAGE, dirPath)
    logging.debug("Target directory path: {}".format(targetPath))
    if not os.path.exists(targetPath):
        logging.debug("Creating target directory {}".format(targetPath))
        os.makedirs(targetPath)
    targetFile = os.path.join(BASE_STORAGE, refPath)
    logging.debug("Target file: {}".format(targetFile))
    force = CONF.get("force")
    doThumb = True
    if os.path.exists(targetFile):
        if not force:
            logging.debug("File already exist: skipping it. Use -f to force")
            doThumb = False
        else:
            logging.debug("Force overwrite of {}".format(targetFile))
    if doThumb:
        thumb_image_secured(filePath, targetFile)

# All parameters must have been properly checked before calling this function
def thumb_image_secured(source, target):
    logging.info("Creating thumbnail for {}".format(source))
    size_conf = CONF.get("size")
    size = size_conf, size_conf
    logging.debug("Opening image {}".format(source))
    im = Image.open(source)
    logging.debug("Creating thumbnail")
    im.thumbnail(size)
    logging.debug("Saving image to {}".format(target))
    im.save(target)

if __name__ == "__main__":
    main()
