# deploy/fabric needs
from fabric.api import *

# deploy directory and repo info
code_dir_root = '/path/to/code/directory'
code_dir_target = '/path/to/code/directory/target'
code_repo = 'git@gitrepo.com:user/REPO.git'

# how many hosts you want to handle concurrently
pool_size = 5


# remote server configs
def prod():
    env.user = 'username'
    env.hosts = ['domain.com']
    env.key_filename = '/path/to/.ssh/id_rsa'


def staging():
    env.user = 'username'
    env.hosts = ['domain.com']
    env.key_filename = '/path/to/.ssh/id_rsa'
