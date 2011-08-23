Boston Data Catalog
===================

A Django web application that can be used by cities to easily get an
open data catalog up and running.


Setup Instructions
------------------

You should first make sure that you have [`git` installed on your
computer](http://git-scm.com/), so that you can clone the project.

    $ git clone git://github.com/codeforamerica/Open-Data-Catalog.git open_data_catalog
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

    $ python manage.py syncdb
    $ python manage.py migrate

You can then start up the development server.

    $ python manage.py runserver

You should then be able to use your web browser to pull up the
application.


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
