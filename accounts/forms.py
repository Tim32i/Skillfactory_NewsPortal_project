from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class SignupForm_Author(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(SignupForm_Author, self).save()
        authors = Group.objects.get(name='authors')
        user.groups.add(authors)
        if commit:
            user.save()

        return user
