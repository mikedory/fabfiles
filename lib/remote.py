# import the fabric requirements
from __future__ import with_statement
from fabric.api import *

# import local_settings.py
from config.local_settings import *


# drop the code off on the remote server
def code_deploy(tag=None, branch=None):
    # when deploying by tag
    if tag is not None:
        # define where this is all going
        code_deploy_dir = code_dir_root + "/" + tag
        print "*** deploying %s to %s ***" % (tag, code_deploy_dir)

        # make the directory, deploy the code, and symlink it
        run('mkdir -p %s' % code_deploy_dir)
        with cd(code_dir_root):
            run("git clone %s %s" % (code_repo, code_deploy_dir))
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
                run("git clone %s %s" % (code_repo, code_dir_target))
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
    code_deploy_dir = code_dir_root + "/" + tag
    with cd(code_dir_root):
        run("ln -nfs %s %s" % (code_deploy_dir, code_dir_target))


def minify():
    # this is where one would pack/minify stuff
    pass


# restart the supervisor process
def supervisor_restart():
    # restart processes and clean up
    print "*** restarting server ***"
    run("supervisorctl restart %s" % supervisor_app)
