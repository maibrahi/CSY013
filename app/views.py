import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login
from django.shortcuts import render_to_response

from .utils import common_context

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
from social_django.utils import psa, load_strategy

from .decorators import render_to

from .models import Module, Student

def general_context(request, view_vars):
    return common_context(
        settings.AUTHENTICATION_BACKENDS,
        load_strategy(),
        request.user,
        plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        # **out,
        **view_vars
    )


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@render_to('login.html')
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('/modules')


@login_required
@render_to('login.html')
def done(request):
    """Login complete view, displays user data"""
    pass


@render_to('login.html')
def validation_sent(request):
    """Email validation sent confirmation page"""
    return {
        'validation_sent': True,
        'email': request.session.get('email_validation_address')
    }


@render_to('login.html')
def require_email(request):
    """Email required page"""
    strategy = load_strategy()
    partial_token = request.GET.get('partial_token')
    partial = strategy.partial_load(partial_token)
    return {
        'email_required': True,
        'partial_backend_name': partial.backend,
        'partial_token': partial_token
    }


@psa('social:complete')
def ajax_auth(request, backend):
    """AJAX authentication endpoint"""
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.POST.get('access_token'),
            'oauth_token_secret': request.POST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.POST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')


# Modules

@login_required
# @render_to('modules/index.html')
def modules_index(request):
    modules = Module.objects.all()

    return render(
        request,
        'modules/index.html',
        general_context(request, {"modules": modules})
    )

@login_required
# @render_to('modules/modules_students.html')
def modules_students(request, module_id):
    code = Module.objects.get(pk=module_id).code
    students = Module.objects.get(pk=module_id).get_students()
    return render(
        request,
        'modules/module_students.html',
        general_context(request, {"students": students, "code": code})
    )

@login_required
# @render_to('modules/modules_students.html')
def students_list(request):
    all_students = Student.objects.all()
    return render(
        request,
        'modules/students.html',
        general_context(request, {"students": all_students})
    )
