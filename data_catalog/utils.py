"""Utility functions used by the data catalog."""

from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import force_unicode
from django.utils.simplejson import dumps, JSONEncoder


def render_response(request, *args, **kwargs):
    """
    Django Snippet:  http://djangosnippets.org/snippets/3/

    Simplified `render_to_response` function that doesn't require the
    request `context_instance` to always be reset to `RequestContext`.
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)


# The following snippets are taken from:
# http://djangosnippets.org/snippets/2411/

def jsonify_model(model):
    """Turn a model into a serializable dict."""
    model_dict = model.__dict__
    for key, value in model_dict.items():
        if key.startswith('_'):
            del model_dict[key]
        else:
            model_dict[key] = force_unicode(value)
    return model_dict


class API_JSONEncoder(JSONEncoder):
    """Help encode data into JSON."""
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return [jsonify_model(o) for o in obj]
        if isinstance(obj, Model):
            return jsonify_model(obj)
        return JSONEncoder.default(self, obj)


class JSONResponse(HttpResponse):
    """Return an HTTP response that's JSON content."""
    status_code = 200

    def __init__(self, data):
        json_response = dumps(data, ensure_ascii=False, indent=2, cls=API_JSONEncoder)
        HttpResponse.__init__(self, json_response, mimetype="text/javascript")
