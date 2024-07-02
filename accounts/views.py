from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.views.generic.edit import CreateView
from .forms import SignupForm_Author

class Signup_Author(CreateView):
    model = User
    form_class = SignupForm_Author
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Перед регистрацией, если залогинен пользователь, разлогиниваем его
        if self.request.user.id is not None:
            for s in Session.objects.all():
                data = s.get_decoded()
                if int(data.get('_auth_user_id', None)) == int(self.request.user.id):
                    s.delete()

        return super().form_valid(form)


def logout_redirect(request):
    if request.user.id is not None:
        for s in Session.objects.all():
            data = s.get_decoded()
            data_get = data.get('_auth_user_id', None)
            if data_get is None:
                continue
            if int(data_get) == int(request.user.id):
                s.delete()

    response = redirect('/news/')
    return response





