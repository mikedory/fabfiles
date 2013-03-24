# import the fabric requirements
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

# import local_settings.py
from config.local_settings import *


# ---------------------------------------------------------

"""
Test and prepare everything locally using Django's test framework
Then, commit files, and push to Github
"""


# run Django's test framework
def test():
    with settings(warn_only=True):
        result = local('./manage.py test %s' % django_app, capture=True)
    if result.failed and not confirm("Tests failed! D: Continue anyway?"):
        abort("Aborting!")


# add and commit all local files
def commit():
    with settings(warn_only=True):
        commit = local("git add -p && git commit")
    if commit.failed:
        print("Nothing to commit. Moving on.")


# push up to github
def push():
    local("git push origin master")


# run all the pre-flight tests
def prepare_deploy():
    test()
    commit()
    push()

# ---------------------------------------------------------

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


# ---------------------------------------------------------

# run the code deploy, then restart the supervisor process
@parallel(pool_size=pool_size)
def deploy(tag=None, branch=None):
    code_deploy(tag, branch)
    minify()
    supervisor_restart()


# roll back to a specific tag
@parallel(pool_size=pool_size)
def rollback(tag=None):
    code_rollback(tag)
    supervisor_restart()
