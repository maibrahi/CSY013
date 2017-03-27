import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login
from django.shortcuts import render_to_response
from django.contrib import messages

from .utils import common_context

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
from social_django.utils import psa, load_strategy

from .decorators import render_to

from .models import *
from .forms import *

from attendance import *

import pdb

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
def modules_index(request):
    modules = Module.objects.all()

    return render(
        request,
        'modules/index.html',
        general_context(request, { "modules": modules })
    )

@login_required
def modules_show(request, **kwargs):
    messages.add_message(request, messages.INFO, 'Hello world.')
    module = Module.objects.get(pk=kwargs["id"])

    students = module.get_students()

    return render(
        request,
        'modules/show.html',
        general_context(request, {
            "module": module,
            "students": students,
            "timeslots": module.timeslot_set.all().order_by("start_time")
        })
    )

@login_required
def students_index(request, **kwargs):
    students = Student.objects.all()

    return render(
        request,
        'students/index.html',
        general_context(request, {
            "students": students,
        })
    )

@login_required
def students_show(request, **kwargs):
    student = Student.objects.get(pk=kwargs["id"])

    modules = student.get_modules()
    module_ids = [module.id for module in modules]

    return render(
        request,
        'students/show.html',
        general_context(request, {
            "modules": modules,
            "student": student,
            "timeslots": student.get_timeslots()
        })
    )


@login_required
def timeslots_show(request, **kwargs):
    try: # get the timeslot
        timeslot = TimeSlot.objects.get(pk=kwargs["id"])
    except TimeSlot.DoesNotExist:
        raise Http404("TimeSlot not found.")

    if not timeslot.is_sheet_generated():
        timeslot.capture_student_ids()
        timeslot.save()

    students = timeslot.get_students()

    return render(
        request,
        'timeslots/show.html',
        general_context(request, {
            "slot": timeslot,
            "form": SheetImageForm(),
            "students": students,
            "module": timeslot.module
        })
    )


@login_required
def timeslots_sheet_upload(request, **kwargs):
    try: # get the timeslot
        timeslot = TimeSlot.objects.get(pk=kwargs["id"])
    except TimeSlot.DoesNotExist:
        raise Http404("TimeSlot not found.")

    if request.method != 'POST':
        raise Http404("POST ONLY")

    form = SheetImageForm(request.POST, request.FILES)
    if form.is_valid():
        # pdb.set_trace()
        # form.save()
        # form.cleaned_data['image'].file

        # page_index = int(form.cleaned_data["page_index"])

        a = Attendance()
        sheet_list = [form.cleaned_data['image'].file]
        attendance_list = a.get_attendance_list(sheet_list, len(timeslot.ordered_student_ids))


        print(attendance_list)
        timeslot.ordered_attendance = attendance_list
        # print(page_index)
        timeslot.save()

        # return redirect('home')
        return redirect("timeslots_show", id=timeslot.id)
    else:
        raise Http404("FileUpload error")


@login_required
def sheet(request, **kwargs):
    # module = Module.objects.get(pk=kwargs["id"])

    try: # get the timeslot
        timeslot = TimeSlot.objects.get(pk=kwargs["id"])
    except TimeSlot.DoesNotExist:
        raise Http404("TimeSlot not found.")

    if "page_number" not in kwargs: # redirect to page 1 if no page given
        return redirect("sheet_show", id=timeslot.id, page_number=1)

    students = list(timeslot.get_students())
    page_count = timeslot.sheet_page_count()

    try: # validate pagenumber
        page_number = int(kwargs["page_number"])
        if page_number > page_count or page_number < 1:
            raise(ValueError)
    except ValueError as e:
        raise Http404("Sign in sheet page not found!")

    # page_number 1 is page_index 0...
    page_index = page_number - 1

    offset = 10 * page_index
    students_for_page = students[(offset):(offset + 10)]

    # table_rows = [[s.name(), s.id, ''] for s in students]

    return render(
        request,
        'timeslots/sheet.html',
        general_context(request, {
            "slot": timeslot,
            "students": students_for_page,
            # "page_index": page_index,
            "page_number": page_number,
            "page_count": page_count
        })
    )
