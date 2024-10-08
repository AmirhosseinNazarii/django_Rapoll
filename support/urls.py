from django.urls import path
from . import views

urlpatterns = [
    path('', views.support, name='support'),
    path('send-ticket/', views.send_ticket, name='send_ticket'),
    path('close-ticket/<int:ticket_id>/', views.close_ticket, name='close_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]
