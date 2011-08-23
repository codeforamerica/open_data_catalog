"""Context processors for the data catalog."""

from django.conf import settings


def settings_context(request):
    """
    Exposes specific project settings in a `TEMPLATE_CONTEXT_SETTINGS` iterable
    in your settings.py file to a `settings` variable to all templates.
    """
    context_settings = {}
    for value in settings.TEMPLATE_CONTEXT_SETTINGS:
        context_settings[value] = getattr(settings, value)
    return {'settings': context_settings}
