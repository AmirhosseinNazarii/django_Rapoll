from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('login/', views.login, name='login'),  # اضافه کردن مسیر لاگین
    path('main/', views.main, name='main'),     # اضافه کردن مسیر صفحه اصلی
    path('logout/', views.logout, name='logout'),  # مسیر خروج
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('block-search/', views.block_search, name='block_search'),
    path('get_neighborhoods/', views.get_neighborhoods, name='get_neighborhoods'),
    path('get_streets/', views.get_streets, name='get_streets'),
    path('get_alleys/', views.get_alleys, name='get_alleys'),
    path('search_blocks/', views.search_blocks, name='search_blocks'),
    path('buy_block/', views.buy_block, name='buy_block'),
    path('finalize_purchase/', views.finalize_purchase, name='finalize_purchase'),

]
