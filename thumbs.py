import sys
import pyparams #https://github.com/jbrendel/pyparams
import os
import logging
from PIL import image #https://pillow.readthedocs.io/en/3.1.x/reference/Image.html

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
                "default"   : None,
                "conffile"  : None,
                "cmd_line"  : ('p', 'filePath')
                },
            "force" : {
                "default"   : None,
                "param_type": param.PARAM_TYPE_BOOL,
                "cmd_line"  : ('f', 'force')
                },
            "size" : {
                "default"   : 128,
                "param_type": param.PARAM_TYPE_INT,
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
        logging.debug("file path mode: {}".format(filePath))
        thumb_file(filePath)

def thumb_file(filePath):
    logging.info("Scanning file path: {}".format(filePath))
    if not os.path.isfile(filePath):
        logging.info("Not a file path")
        sys.exit(1)
    filename, extension = os.path.splitex(filePath)
    if not extension == "jpg":
        logging.info("Bad file extension. Only jpg supported")
        sys.exit(1)
    dirPath = os.path.dirname(filePath)
    targetPath = os.path.join(BASE_STORAGE, dirPath)
    if not os.path.exists(targetPath):
        logging.debug("Creating target directory {}".format(targetPath))
        os.makedirs(targetPath)
    targetFile = os.path.join(BASE_STORAGE, filePath)
    force = CONF.get("force")
    if os.path.exists(targetFile):
        if not force:
            logging.warning("File already exist: skipping it. Use -f to force")
            sys.Exit(1)
        else:
            logging.debug("Force overwrite of {}".format(targetFile))
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
