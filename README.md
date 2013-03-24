Fabfiles
========

Because deploying Django apps with Fabric is *fun!*


Installation
------------

Because it's *always* a handy way to avoid conflicts, virtualenv is recommended:

    pip install virtualenv

Then set up a virtualenv for the app, and activate it:

    virtualenv venv --distribute && source ./venv/bin/activate 
    # run "deactivate" to turn it off

Then to get the dependencies for this application, install the remaining requirements via Pip:

    pip install -r requirements.txt


