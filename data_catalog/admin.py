"""Admin interface for the data catalog."""

from django.contrib import admin
from data_catalog.models import App, Data, Project


admin.site.register((App, Data, Project))
