import subprocess
from uuid import uuid4

def run():

    session_uuid = uuid4()
    #vyos_shell_api = foo.set_config_params('bin','shell_api_path')
    # Obtain session environment
    vyos_shell_api = '/bin/cli-shell-api'
    set_session_env_cmd = "eval `{} getSessionEnv {}`\n".format(vyos_shell_api, session_uuid)

    # Spawn a bash shell
    vbash = subprocess.Popen('/bin/bash', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE) 

    # Evaluate environment string
    vbash.stdin.write(set_session_env_cmd)

    # Setup the session
    setup_session_cmd = "{} setupSession\n".format(vyos_shell_api)
    vbash.stdin.write(setup_session_cmd)

    # Check if session is set up
    vbash.stdin.write("{} inSession\n".format(vyos_shell_api))
    vbash.stdin.write("echo $?\n")
    print vbash.stdout.readline()

    # teardownSession
    vbash.stdin.write("{} teardownSession\n".format(vyos_shell_api))
    
    vbash.stdin.write("{} inSession\n".format(vyos_shell_api))
    vbash.stdin.write("echo $?\n")
    print vbash.stdout.readline() 

run()
