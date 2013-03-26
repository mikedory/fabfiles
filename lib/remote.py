# import the fabric requirements
from __future__ import with_statement
from fabric.api import *

# import local_settings.py
from config.local_settings import *

# import os for file-joining fun
from os import path


# get everything ready in virtualenv land
def virtualenv_check():
    print "*** checking virtualenv dependencies ***"

    # make sure virtualenv is set up on the machine in question
    with settings(warn_only=True):
        if run("pip freeze | grep virtualenv").failed:
            sudo("pip install virtualenv")

    # test the venv directory too
    with settings(warn_only=True):
        if run("test -d %s" % code_venv_dir).failed:
            with cd(code_dir_target):
                run("virtualenv venv --distribute")


def virtualenv_activate():
    print "*** activating virtualenv ***"

    # activate the virtualenv, and install the required code
    run("source %s/bin/activate" % code_venv_dir)
    run("pip install -r %s/requirements.txt" % code_dir_target)


# drop the code off on the remote server
def code_deploy(tag=None, branch=None):
    # when deploying by tag
    if tag is not None:
        # define where this is all going
        code_deploy_dir = path.join(code_dir_root, tag)
        print "*** deploying %s to %s ***" % (tag, code_deploy_dir)

        # make the directory, deploy the code, and symlink it
        run('mkdir -p %s' % code_deploy_dir)
        with cd(code_dir_root):
            run("git clone --depth 1 %s %s" % (code_repo, code_deploy_dir))
        with cd(code_deploy_dir):
            run("git checkout %s" % tag)
        with cd(code_dir_root):
            run("ln -nfs %s %s" % (code_deploy_dir, code_dir_target))

    # when deploying by branch
    elif branch is not None:
        print "*** deploying %s to %s ***" % (branch, code_dir_target)

        # test to make sure the repo exists
        with settings(warn_only=True):
            if run("test -d %s" % code_dir_target).failed:
                run("git clone --depth 1 %s %s" % (code_repo, code_dir_target))

        # fetch, checkout, and merge the target branch
        with cd(code_dir_target):
            run("git fetch")
            run("git checkout %s" % branch)
            run("git merge origin/%s" % branch)

    # gotta have one or the other!
    else:
        abort("like, seriously. you need a tag or a branch, brah.")

    print "*** code deployed ***"


# roll back to a previously deployed tag
def code_rollback(tag=None, branch=None):
    code_deploy_dir = path.join(code_dir_root, tag)
    with cd(code_dir_root):
        run("ln -nfs %s %s" % (code_deploy_dir, code_dir_target))


def minify():
    # this is where one would pack/minify stuff
    pass


# restart the supervisor process
def supervisor_restart():
    print "*** restarting supervisor ***"

    # restart the app via supervisor
    run("supervisorctl restart %s" % supervisor_app)
