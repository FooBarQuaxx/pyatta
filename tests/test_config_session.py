import pytest
import os
import sys

sys.path.append('/home/vyos/vyos-api')
import VyosSessionConfig

sessionCfg = VyosSessionConfig.sessionconfig()

def setup():
    """
    Set up a config session
    """
    pass

def teardown():
    """
    Tear down the config session
    """
    pass

def test_config_parser():
    """
    Test if pyatta is well formated. If so, test if some config params
    are correctly set.
    """
    if os.path.isfile('/home/vyos/vyos-api/pyatta.conf'):
        assert sessionCfg.get_config_params('bin','shell_api_path') == '/bin/cli-shell-api'
        
def test_inSession():
    """
    Test if current session is available.
    """
    pass
