# deploy/fabric needs
from fabric.api import *

# deploy directory and repo info
code_dir_root = '/path/to/code/directory'
code_dir_target = '/path/to/code/directory/target'
code_repo = 'git@gitrepo.com:user/REPO.git'
code_venv_dir = '/path/to/code/directory/venv'

# how many hosts you want to handle concurrently
pool_size = 5

# process names
django_app = 'appname'
supervisor_app = 'appname'

# defaults for local fab actions
test_default = True
commit_default = True
push_default = True

# defaults for remote fab actions
supervisor_default = True
virtualenv_default = True


# remote server configs
def prod():
    env.user = 'username'
    env.hosts = ['domain.com']
    env.key_filename = '/path/to/.ssh/id_rsa'


def stg():
    env.user = 'username'
    env.hosts = ['domain.com']
    env.key_filename = '/path/to/.ssh/id_rsa'


def dev():
    env.user = 'username'
    env.hosts = ['domain.com']
    env.key_filename = '/path/to/.ssh/id_rsa'
