from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return redirect('unauthorized')
        return _wrapped_view
    return decorator

def department_required(departments):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'department') and request.user.department in departments:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('Department access denied')
        return _wrapped_view
    return decorator
