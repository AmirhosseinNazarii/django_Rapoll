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
    path('buy-failed/', views.finalize_purchase, name='buy_failed'),  # مسیر جدید برای BuyFailed
    path('buylist/', views.buylist, name='buylist'),  # مسیر جدید برای صفحه buylist
    path('sellblock/', views.sell_block, name='sellblock'),
    path('list_block/<int:block_id>/', views.list_block, name='list_block'),
    path('buy_from_user/', views.buy_from_user, name='buy_from_user'),  # مسیر خرید از کاربر
    path('final_buy_from_user/', views.final_buy_from_user, name='final_buy_from_user'),
    path('support/', views.support, name='support'),  # صفحه پشتیبانی
    path('send_ticket/', views.send_ticket, name='send_ticket'),  # ارسال تیکت
    path('send_ticket/<int:ticket_number>/', views.send_ticket_detail, name='send_ticket_detail'),  # جزئیات تیکت
    path('close_ticket/<int:ticket_number>/', views.close_ticket, name='close_ticket'),  # بستن تیکت
     path('block-search-id/', views.block_search_id, name='block_search_id'),

    

]
