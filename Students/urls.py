from django.urls import path, re_path
from . import views
from .views import Subject_view
from .views import home, Message

urlpatterns = [
    path('home/', home, name='home'),
    path('Subject_view/', Subject_view, name='Subject_view'),
    path('Message/', Message, name='Message'),
]
    