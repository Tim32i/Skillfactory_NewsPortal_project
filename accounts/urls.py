from django.urls import path
from .views import Signup_Author, logout_redirect

urlpatterns = [
    path('signup_author/', Signup_Author.as_view(), name='signup_author'),
    path('logout/', logout_redirect)
]