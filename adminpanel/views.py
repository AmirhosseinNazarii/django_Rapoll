# adminpanel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User, UserDetails
from .models import Block  # اضافه کردن مدل بلوک
from django.contrib import messages  # برای استفاده از سیستم پیام‌رسانی

from django.http import HttpResponseForbidden
from users.models import Ticket, TicketMessage

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

# بررسی ادمین بودن
def is_admin(user):
    return user.is_admin

def admin_tickets(request):
    # بررسی اینکه آیا کاربر لاگین کرده است یا خیر
    if 'user_id' not in request.session:
        return redirect('login')  # اگر کاربر لاگین نکرده است، به صفحه لاگین هدایت شود
    
    # دریافت اطلاعات کاربر از سشن
    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)

    # بررسی اینکه آیا کاربر ادمین است یا خیر
    if not user.is_admin:
        return HttpResponseForbidden("شما به این بخش دسترسی ندارید.")  # در صورت نبود دسترسی پیام خطا نمایش داده شود

    # نمایش لیست تیکت‌ها برای ادمین
    tickets = Ticket.objects.all()
    return render(request, 'adminpanel/admins.html', {'tickets': tickets})



def response_ticket(request, ticket_id):
    # بررسی لاگین بودن کاربر
    if 'user_id' not in request.session:
        return redirect('login')
    
    # دریافت اطلاعات کاربر
    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)

    # بررسی اینکه آیا کاربر ادمین است
    if not user.is_admin:
        return HttpResponseForbidden("شما به این بخش دسترسی ندارید.")

    ticket = get_object_or_404(Ticket, id=ticket_id)
    messages = TicketMessage.objects.filter(ticket=ticket)

    if request.method == 'POST':
        message_content = request.POST.get('message')
        file = request.FILES.get('file')

        if message_content:
            TicketMessage.objects.create(
                ticket=ticket,
                user=user,  # فرستنده ادمین است
                message=message_content,
                file=file
            )
            return redirect('response_ticket', ticket_id=ticket.id)

    return render(request, 'adminpanel/response.html', {'ticket': ticket, 'messages': messages})
