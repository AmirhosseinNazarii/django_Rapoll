from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('login/', views.login, name='login'),  # اضافه کردن مسیر لاگین
    path('main/', views.main, name='main'),     # اضافه کردن مسیر صفحه اصلی
    path('logout/', views.logout, name='logout'),  # مسیر خروج
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]
