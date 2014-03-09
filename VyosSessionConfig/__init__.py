#!../bin/python
import os
import ConfigParser


PROJECT_PATH = "/home/vyos/vyos-api"
CONFIG_FILE_NAME = "pyatta.conf"

class sessionconfig():
    """
    Class docstring goes here..
    """

    def get_config_params(self, section, key):
        """
        Method docstring goes here
        """
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(os.path.join(PROJECT_PATH, CONFIG_FILE_NAME)))
        return config.get(section, key)

    def setup_config_session(self, shell_api_path):
        """
        Method docstring goes here
        """
        return ("""
            session_env=$(%s getSessionEnv $PPID) 
            eval $session_env 
            %s setupSession
        """ % (shell_api_path, shell_api_path))
