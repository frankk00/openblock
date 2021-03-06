==========================================
Creating a Custom Site Based on OpenBlock
==========================================

If you want to do something much different than
:doc:`packages/obdemo`, you're better off starting from scratch with a
custom Django app. We provide a script that will get you started with
a skeleton app you can edit.

Setting up the app
==================

Begin by :doc:`preparing your system <setup>`, including setting up
and activating a virtualenv.

Now install the core OpenBlock python packages::

   $ cd $VIRTUAL_ENV
   $ mkdir -p src/
   $ git clone git://github.com/openplans/openblock.git src/openblock

``Pip`` can install OpenBlock and the rest of our Python dependencies with a few
commands::

  $ cd $VIRTUAL_ENV/src/openblock
  $ pip install -r ebpub/requirements.txt -e ebpub
  $ pip install -r ebdata/requirements.txt -e ebdata
  $ pip install -r obadmin/requirements.txt -e obadmin

Now do the following to create a new openblock project.  **Note**:
Your project name should be suitable for use as a python module name;
i.e. no spaces etc.  Here we assume the project name is `myblock`::

    $ cd $VIRTUAL_ENV/src
    $ paster create -t openblock myblock

After answering a few questions, this will create a bare-bones Django
project in the folder you
specified.  Next, install the project into your environment::

    $ cd myblock
    $ python setup.py develop
    ...

Your django settings are located in settings.py within your project.  You should review these
and make adjustments based on your setup::

    $ <favorite_editor> myblock/settings.py
    ...

Read more about :doc:`important settings you can/should customize <configuration>`.

Now, as usual with Django projects, you'll need to create and
initialize your database(s).  If you haven't changed the default
database settings, and if you've followed the :ref:`template_setup`
instructions, then the database creation command would simply be::

    $ createdb -T template_postgis openblock_myblock

Initializing the database(s) must be done in the right order::

    $ export DJANGO_SETTINGS_MODULE=myblock.settings
    $ django-admin.py syncdb --migrate


To create an administrative user, use the standard django createsuperuser command.  This will ask for slightly different information than normal because OpenBlock's user system is based on email::

    $ django-admin.py createsuperuser
    ...

Starting the Test Server
------------------------

Run django's test server using your project's settings and visit http://127.0.0.1:8000/ in your Web browser to see the site in action (with no data)::

    $ export DJANGO_SETTINGS_MODULE=myblock.settings
    $ django-admin.py runserver
    ...
    Development server is running at http://127.0.0.1:8000/

You can now log into your openblock instance and visit the administrative site at http://127.0.0.1:8000/admin/


Loading Data: Things You Will Need
==================================

To get anything useful out of your site, at minimum you will need the following:

 1. A database of streets in your city; for example
    TIGER/Line files from http://www.census.gov/geo/www/tiger/ .
    See :ref:`blocks`.

 2. Shapefiles with areas of interest - for example,
    neighborhoods, zip codes etc.
    See :ref:`locations`.

 3. Sources of news data to feed in.

    a. Configure the system with schemas for them.
       See :doc:`schemas` and ebpub docs for :ref:`newsitem-schemas`.

    b. Write scraper scripts to retrieve news from your news sources and load
       it into the database. See the :doc:`scraper_tutorial`, :doc:`packages/ebdata`
       and http://developer.openblockproject.org/wiki/ScraperScripts .

 4. Optionally, customize the look and feel of the site.
    See the ebpub docs for :ref:`custom-look-feel`.

Gathering all this data and feeding it into the database can be a bit
of work at this point.  The ``obdemo/bin/bootstrap_demo.sh`` script
does all this for the demo site with Boston data, by calling other
scripts; together, they should serve as a decent example of how to do
things in detail.

If you want to load the demo data into your project, you can use the steps 
listed in :ref:`demodata`. **Note**: use the settings module for your project
instead of `obdemo.settings`.


Additional Resources
====================

For more documentation (in progress), see also:
    * http://developer.openblockproject.org/wiki/Data
    * http://developer.openblockproject.org/wiki/Ideal%20Feed%20Formats
