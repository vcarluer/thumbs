import sys
import pyparams

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

def main():
    CONF.acquire(sys.argv[1:])
    print(CONF.get("filePath"))

if __name__ == "__main__":
    main()
