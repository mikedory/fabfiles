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


Use
---

### Local

#### Preparing for a deploy

This application assumes you're using Django, so we'll use its test framework to ensure everything is kosher first.  Then, we'll commit everything, and push it up to Github


### Remote

#### Deploying code

To deploy a tag:

    fab env deploy:tag=YYYY-MM-DD-tag-description

To deploy a branches:

    fab deploy:branch=master

So to deploy a tag to production, you can run:

    fab prod deploy:tag=YYYY-MM-DD-tag-description

And to deploy to a single server:

    fab -u username -H domain.com -i /path/to/.ssh/id_rsa deploy:tag=YYYY-MM-DD-tag-description


#### Restarting processes 

You can restart supervisor in a standalone fashion easily:

    fab supervisor_restart

#### Rolling back

Rolling back to a previously-deployed tag is something one must occasionally do if the impossible event of a bad deploy happens.  No worries tho, it's easy!

    fab rollback:tag=YYYY-MM-DD-tag-description
