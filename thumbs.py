import sys
import pyparams
import os
import logging

logging.basicConfig(level = logging.DEBUG)

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
            "filePath" : {
                "default"   : None,
                "conffile"  : None,
                "cmd_line"  : ('f', 'filePath')
                }
            }
        )
print("THUMBS")
print("--------------------------------------------------------")
print("Available parameters:")
print(CONF.make_doc())
print("--------------------------------------------------------")

def main():
    CONF.acquire(sys.argv[1:])
    if CONF.get("filePath"):
        filePath = CONF.get("filePath")
        logging.debug("file path mode: {}".format(filePath))
        print("Scanning file path: {}".format(filePath))
        if not os.path.isfile(filePath):
            print("Not a file path")
            sys.exit(1)


if __name__ == "__main__":
    main()
