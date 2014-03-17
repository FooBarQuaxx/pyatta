#!../bin/python
import os
import ConfigParser
from uuid import uuid4
import subprocess

PROJECT_PATH = "/home/vyos/vyos-api"
CONFIG_FILE_NAME = "pyatta.conf"

def _run(cmd, output=False):
    """
    To run command easier
    """
    if output:
        try:
            out = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            out = False
            return out
    try:
        out = subprocess.check_call(cmd, shell=True) # returns 0 for True
    except subprocess.CalledProcessError:
        out = 1
    return out

def get_config_params(section, key):
    """
    To get specific parameters valuers from config file 
    """
    config = ConfigParser.SafeConfigParser()
    config.readfp(open(os.path.join(PROJECT_PATH, CONFIG_FILE_NAME)))
    return config.get(section, key)

vyos_shell_api_path = get_config_params('bin','shell_api_path')

class SessionAlreadyExists(Exception): pass
class SetupSessionFailed(Exception): pass

class Session(object):
    """
    Return the session instance if exists. Else, create new one.
    SessionAlreadyExists exception raised on the second instantiation.
    """
    _ref = None
    def __new__(cls, *args, **kw):
        if cls._ref is not None:
            raise SessionAlreadyExists('[WARN] A session exist already !')
        cls._ref = super(Session, cls).__new__(cls, *args, **kw)
        return cls._ref

class sessionconfig(Session):
    """
    Create and manage a Vyos config session.
    To create instance call setup_config_session() method.
    """

    def setup_config_session(self):
        """
        Setup vyos session. A random uuid is generated as a sesssion identifier 
        ($PPID -Shell PID- could be used as well).
        """
        identifier = uuid4()
        env = {}
        env['VYATTA_CHANGES_ONLY_DIR'] = '/opt/vyatta/config/tmp/changes_only_{}'.format(identifier)
        env['VYATTA_CONFIG_TEMPLATE'] = '/opt/vyatta/share/vyatta-cfg/templates'
        env['VYATTA_ACTIVE_CONFIGURATION_DIR'] = '/opt/vyatta/config/active'
        env['VYATTA_EDIT_LEVEL'] = '/'
        env['VYATTA_TEMP_CONFIG_DIR'] = '/opt/vyatta/config/tmp/new_config_{}'.format(identifier)
        env['VYATTA_TEMPLATE_LEVEL'] = '/'
        env['VYATTA_CONFIG_TMP'] = '/opt/vyatta/config/tmp/tmp_{}'.format(identifier)
        # Add vyos session environment to system environment. This is not good but actually it seems
        # that is the only way to handle a persistant vyos session after spawning a shell.
        os.environ.update(env)
        # Spawn shell and setup vyos config session
        if _run('{} setupSession'.format(vyos_shell_api_path)):
            # Unset vyos session environment and raise an exception
            for key in env.keys(): del os.environ[key]
            raise SetupSessionFailed('[ERROR] Could not create session !')
        self.session_id = identifier
        self.session_envs = env
        return True

    def session_exists(self):
        """
        Test if a vyos config session is set up
        """
        return True if _run('{} inSession'.format(vyos_shell_api_path)) == 0 else False

    def teardown_config_session(self):
        """
        End current configuration session.
        """
        _run('{} teardownSession'.format(vyos_shell_api_path))
        for key in self.session_envs.keys(): del os.environ[key]
        return True
