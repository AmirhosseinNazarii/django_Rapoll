# adminpanel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('panel1/', views.panel1, name='panel1'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('toggle_status/<int:user_id>/', views.toggle_status, name='toggle_status'),
    path('add_block/', views.add_block, name='add_block'),

]
