# adminpanel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User, UserDetails
from .models import Block  # اضافه کردن مدل بلوک
from django.contrib import messages  # برای استفاده از سیستم پیام‌رسانی

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

def add_block(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        neighborhood = request.POST.get('neighborhood')
        street = request.POST.get('street')
        alley = request.POST.get('alley')
        block_number = request.POST.get('block_number')
        price = request.POST.get('price')

        if city and neighborhood and street and alley and block_number and price:
            try:
                # ایجاد بلوک جدید
                Block.objects.create(
                    city=city,
                    neighborhood=neighborhood,
                    street=street,
                    alley=alley,
                    block_number=block_number,
                    price=price,
                    status=False  # به صورت پیش‌فرض قابل فروش باشد
                )
                messages.success(request, "بلوک جدید با موفقیت اضافه شد.")
                return redirect('panel1')
            except Exception as e:
                messages.error(request, f"خطا در اضافه کردن بلوک: {str(e)}")
        else:
            messages.error(request, "لطفاً همه فیلدها را پر کنید.")

    return redirect('panel1')