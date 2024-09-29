from django.urls import path
from . import views

urlpatterns = [
    path('panel1/', views.panel1, name='panel1'),
]
