# import the fabric requirements
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

# import local_settings.py
from config.local_settings import *


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
