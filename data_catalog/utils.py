"""Utility functions used by the data catalog."""

from django.shortcuts import render_to_response
from django.template import RequestContext


def render_response(request, *args, **kwargs):
    """
    Django Snippet:  http://djangosnippets.org/snippets/3/

    Simplified `render_to_response` function that doesn't require the
    request `context_instance` to always be reset to `RequestContext`.
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)
