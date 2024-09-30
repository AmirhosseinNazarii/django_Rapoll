# adminpanel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User, UserDetails


def panel1(request):
    users = User.objects.all()
    return render(request, 'adminpanel/panel1.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.balance = request.POST.get('balance')

        # ویرایش رمز عبور فقط در صورت وارد کردن مقدار جدید
        password = request.POST.get('password')
        if password:
            user.password = password
        
        user.is_admin = request.POST.get('is_admin') == '1'  # تبدیل به Boolean
        user.status = request.POST.get('status') == '1'  # تبدیل به Boolean
        user.save()
        
        # به‌روزرسانی اطلاعات UserDetails
        details = user.details
        details.full_name = request.POST.get('full_name')
        details.last_name = request.POST.get('last_name')
        details.national_code = request.POST.get('national_code')
        details.card_number = request.POST.get('card_number')
        details.phone_number = request.POST.get('phone_number')

        # بارگذاری مجدد کارت ملی اگر فایلی بارگذاری شده باشد
        if 'national_card' in request.FILES:
            details.national_card = request.FILES['national_card']
        
        details.save()
        return redirect('panel1')
    
    return render(request, 'adminpanel/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('panel1')

def toggle_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = not user.status  # تغییر وضعیت کاربر
    user.save()
    return redirect('panel1')
