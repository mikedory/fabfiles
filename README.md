Fabfiles
========

Because deploying [Django](https://www.djangoproject.com/) apps with [Fabric](http://docs.fabfile.org/) is *fun!*


Installation
------------

First off, you want the source, right?  If you didn't already clone this repo, you can easily drop it off in your local dir like so:

    curl -L 'https://github.com/mikedory/fabfiles/tarball/master' | tar zx && mv mikedory-fabfiles-* fabfiles

Because it's *always* a handy way to avoid conflicts, [virtualenv](http://www.virtualenv.org/) is recommended for managing dependencies and Python versions:

    pip install virtualenv

Then set up a virtualenv for the app, and activate it (you can turn it off later by running `deactivate`):

    virtualenv venv --distribute && source ./venv/bin/activate 

Then to get the dependencies for this application, install the remaining requirements via Pip:

    pip install -r requirements.txt

Make a `local_settings.sample.py` called `local_settings.py`, and edit the environment variables accordingly:

    cp config/local_settings.sample.py config/local_settings.py

That it! You're all set to deploy things!


Use
---

### Local

There's a bunch of stuff one might need to do locally, and thankfully, Fabric makes this easy. Most of this focuses on testing and getting ready for a deploy, but more can be easily added to your liking.


#### Testing your app

There's a ton of great testing options for Django apps, so stub in your framework of choice.  You can run locally with like so:

    fab test


#### Preparing for a deploy

As noted, this application assumes you're using Django, so we'll use its test framework to ensure everything is kosher first.  Then, we'll commit everything, and push it up to Github.  The all-in-one command is:

    fab prepare

---

### Remote

Putting stuff on remote servers and running processes from afar &mdash; the fun part!  This is written assuming you're using [Supervisor](http://supervisord.org/) to control your processes ([Gunicorn](http://gunicorn.org/), [Tornado](http://www.tornadoweb.org/), etc.), though that's easily swap-out-able.


#### Deploying code

To deploy a tag:

    fab env deploy:tag=YYYY-MM-DD-tag-description

To deploy a branches:

    fab prod deploy:branch=master

So to deploy a tag to production, you can run:

    fab prod deploy:tag=YYYY-MM-DD-tag-description

And to deploy to a single server:

    fab -u username -H domain.com -i /path/to/.ssh/id_rsa deploy:tag=YYYY-MM-DD-tag-description


#### Restarting processes 

Restarting services remotely is made a bunch easier via Fabric, and included here is a remote supervisor-restart function:

    fab env restart


#### Rolling back

Rolling back to a previously-deployed tag is something one must occasionally do if the impossible event of a bad deploy happens.  No worries tho, it's easy!

    fab env rollback:tag=YYYY-MM-DD-tag-description


About
-----

This app was assembled by [Mike Dory](https://github.com/mikedory), based on [Jeff Forcier](https://github.com/bitprophet/)'s amazing [Fabric](http://fabfile.org) library. Contributions/edits are always welcome, naturally.
