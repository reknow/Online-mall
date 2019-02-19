from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('info/', info),
    path('site/', site),
    path('order/', order),
]