"""Settings for specific city implementations of the data catalog."""

import os

CITY_NAME = 'Boston'
CATALOG_URL = 'opendataboston.org'


# Number of days for the account activation registration window.
ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = 'admin@' + CATALOG_URL
LOGIN_REDIRECT_URL = '/'

# This should work both locally and on DotCloud.
if os.path.exists('/home/dotcloud/current'):
    DB_PATH = '/home/dotcloud/'
else:
    DB_PATH = ''


__all__ = [
    CITY_NAME, CATALOG_URL, ACCOUNT_ACTIVATION_DAYS, DEFAULT_FROM_EMAIL,
    LOGIN_REDIRECT_URL, DB_PATH
]
