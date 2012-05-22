Open Data Catalog
===================

A Django web application that can be used by cities to easily get an
open data catalog up and running.

NOTE: This fork hasn't been touched since mid-2011.  Instead, please visit:

https://github.com/azavea/Open-Data-Catalog

Setup Instructions
------------------

You should first make sure that you have [`git` installed on your
computer](http://git-scm.com/), so that you can clone the project.

    $ git clone git://github.com/codeforamerica/open_data_catalog.git open_data_catalog
    $ cd open_data_catalog

The next step is to make sure that you have both `pip` and `virtualenv`
installed so you can setup and isolated environment.

    $ sudo easy_install pip
    $ pip install virtualenv

If you get errors from `pip install virtualenv`, you might need to run
the command as superuser:

    $ sudo pip install virtualenv

You can then set up your isolated environment independent of your
system's currently installed Python modules.

    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Next, `pip` can recursively install all the dependencies needed to get
the Open Data Catalog up and running.

    $ pip install -r requirements.txt

Running the Open Data Catalog in development is then pretty simple:

    $ python manage.py schemamigration data_catalog --init
    $ python manage.py syncdb
    $ python manage.py migrate data_catalog

You can then start up the development server.

    $ python manage.py runserver

You should then be able to use your web browser to pull up the
application on `http://localhost:8000`.

If you're looking to change the Open Data Catalog to use your city with
the provided templates, then you simply need to edit the
`data_catalog/settings_city` file. By replacing the `CITY_NAME` and
`CATALOG_URL` variables, you can easily change the default locale of
Boston to your specific location (for instance, the code below changes
it to Tulsa).

    CITY_NAME = 'Tulsa'
    CATALOG_URL = 'opendatatulsa.org'


### Creating the Search Index

In order to use Haystack for search, you'll need to run the following
commands from the command line:

    $ mkdir whoosh
    $ python manage.py rebuild_index

This should create a new search index for your local catalog -- that way
you can search for projects, apps, etc.


### Restarting the Server

If you've closed your terminal -- and therefore killed the running
server -- here's a quick couple steps to get back up running.

Make sure you `cd` into the `open_data_catalog` directory.

    $ cd path/to/open_data_catalog

Now, we need to `source` our virtual environment again.

    $ source env/bin/activate

And then we can run the server once again.

    $ python manage.py runserver


### Adding to the Models

If you need to add or take away from the models that you've already
synced with your database (currently `test.db`) -- then you need to run
the following commands to migrate the changes.

    $ python manage.py schemamigration data_catalog --auto
    $ python manage.py migrate data_catalog


### Uploading to DotCloud ###

If you've already signed up for an account on DotCloud and installed the
CLI -- `pip install dotcloud` -- then deploying your Open Data Catalog is
pretty straightforward.

    $ dotcloud create opendata
    $ dotcloud push opendata .

You'll then need to make sure your database is synced properly.

    $ dotcloud run opendata.www python current/manage.py syncdb
    $ dotcloud run opendata.www python current/manage.py migrate

You should then be able to visit the URL returned from the previous
`dotcloud push` command and see the Open Data Catalog running in
development mode on DotCloud's servers.
