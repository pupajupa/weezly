from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def login_required_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to perform this action.', 'danger')
            return redirect('accounts:user_login')  # или любая другая ссылка, например: reverse('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view