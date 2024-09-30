# adminpanel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User, UserDetails


def panel1(request):
    users = User.objects.all()
    return render(request, 'adminpanel/panel1.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # کد ویرایش کاربر
    return redirect('panel1')

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('panel1')

def toggle_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = not user.status  # تغییر وضعیت کاربر
    user.save()
    return redirect('panel1')
