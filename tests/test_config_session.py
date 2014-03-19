import pytest
import os
import sys
import uuid
sys.path.append('/home/vyos/vyos-api')
from VyosSessionConfig import configsession as vsc
from VyosSessionConfig import utils

sessionCfg = None

def setup_module(module):
    """
    Set up a config session
    """
    global sessionCfg
    sessionCfg = vsc.ConfigSession()

def setup_function(function):
    """
    """
    pass

def teardown_function(function):
    """
    """
    pass

def teardown_module(module):
    """
    teardown created config session
    """
    global sessionCfg
    utils.clean_environ(sessionCfg.session_envs)
    del sessionCfg

def test_config_parser():
    """
    Test if some config params are correctly set.
    """
    if os.path.isfile('/home/vyos/vyos-api/pyatta.conf'):
        assert vsc.get_config_params('bin','shell_api_path') == '/bin/cli-shell-api'
        
def test_singleton_session():
    """
    Test if vsc.sessionconfig() is a singleton
    """
    with pytest.raises(vsc.SessionAlreadyExists) as e : 
        vsc.ConfigSession()
    assert e.value.message == '[WARN] A session exist already !'

def test_setup_session():
    """
    Test if vyos session is set up correctely. Check also if environment variables are exists.
    """
    global sessionCfg

    assert sessionCfg.setup_config_session() == True

    for env_var in sessionCfg.session_envs.keys():
        assert sessionCfg.session_envs.get(env_var) == os.environ.get(env_var)
    ## This test could be extended as follow in order to check if vsc.SetupSessionFailed
    ## exception is raised when attempting to create a vyos session (this is not mandatory).
    #with pytest.raises(vsc.SetupSessionFailed) as e :
    #    sessionCfg.setup_config_session()
    #assert e.value.message == '[ERROR] Could not create session !'

def test_inSession():
    """
    Test if current session is available.
    """
    global sessionCfg
    assert sessionCfg.session_exists() == True
