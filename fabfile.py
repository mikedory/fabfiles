# import the fabric requirements
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

# import local_settings.py
from config.local_settings import *

# import the submodules
import lib.local as local
import lib.remote as remote


"""
Test and prepare everything locally using Django's test framework

Then, commit files, and push to Github
"""


# test the app locally
def test():
    local.test()


# run all the pre-flight tests
def prepare():
    local.test()
    local.commit()
    local.push()


"""
Deploy to the remote server!

For tags:
    fab env deploy:tag=YYYY-MM-DD-tag-description

For branches:
    fab deploy:branch=master

So to deploy a tag to production, run:
    fab prod deploy:tag=YYYY-MM-DD-tag-description

And to deploy to a single server:
    fab -u username -H domain.com -i /path/to/.ssh/id_rsa deploy:tag=YYYY-MM-DD-tag-description
"""


# run the code deploy, then restart the supervisor process
@parallel(pool_size=pool_size)
def deploy(tag=None, branch=None):
    remote.code_deploy(tag, branch)
    remote.minify()
    remote.supervisor_restart()


# roll back to a specific tag
@parallel(pool_size=pool_size)
def rollback(tag=None):
    remote.code_rollback(tag)
    remote.supervisor_restart()


# roll back to a specific tag
@parallel(pool_size=pool_size)
def restart():

    remote.virtualenv_check()
    remote.virtualenv_activate()
    remote.supervisor_restart()


# set up the environment for deploys
@parallel(pool_size=pool_size)
def virtualenv_setup():
    # make sure virtualenv is up and ready
    remote.virtualenv_check()
    remote.virtualenv_activate()
