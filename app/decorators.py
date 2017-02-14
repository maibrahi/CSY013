from functools import wraps

from django.conf import settings
from django.shortcuts import render

from .utils import common_context

from social_django.utils import load_strategy


def render_to(template, view_vars={}):
    """Simple render_to decorator"""
    def decorator(func):
        """Decorator"""
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            """Rendering method"""
            out = func(request, *args, **kwargs) or {}
            if isinstance(out, dict):
                context = common_context(
                    settings.AUTHENTICATION_BACKENDS,
                    load_strategy(),
                    request.user,
                    plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
                    **out,
                    **view_vars
                )

                out = render(request, template, context)
            return out
        return wrapper
    return decorator
