import os
from uuid import uuid4
from utils import get_config_params, _run, clean_environ

VYOS_SHELL_API = get_config_params('bin','shell_api_path')

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

class ConfigSession(Session):
    """
    Create and manage a Vyos config session.
    This is a singleton subclass of Session class which ensures that one and one config session only is opened.
    To create instance you have to call setup_config_session() method.
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
        if _run('{} setupSession'.format(VYOS_SHELL_API)):
            # Unset vyos session environment and raise an exception
            clean_environ(env)
            raise SetupSessionFailed('[ERROR] Could not create session !')
        self.session_id = identifier
        self.session_envs = env
        return True

    def session_exists(self):
        """
        Test if a vyos config session is set up
        """
        return True if _run('{} inSession'.format(VYOS_SHELL_API)) == 0 else False

    def teardown_config_session(self):
        """
        End current configuration session.
        """
        _run('{} teardownSession'.format(VYOS_SHELL_API))
        clean_environ(self.session_envs)
        return True
