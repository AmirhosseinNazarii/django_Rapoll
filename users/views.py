from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import check_password
from django.contrib import messages

from django.contrib.auth.hashers import make_password, check_password


from .models import User
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # هش کردن رمز عبور قبل از ذخیره
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('signup_success')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'users/signup_success.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id  # ذخیره شناسه کاربر در سشن

                # بررسی ادمین بودن
                if user.is_admin:
                    return redirect('panel1')  # هدایت به پنل ادمین
                else:
                    return redirect('main')  # هدایت به صفحه اصلی کاربران عادی
            else:
                messages.error(request, 'رمز عبور اشتباه است.')
        except User.DoesNotExist:
            messages.error(request, 'کاربری با این نام کاربری یافت نشد.')
    return render(request, 'users/login.html')

def main(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        return render(request, 'users/main.html', {'user': user})
    else:
        return redirect('login')
    
def logout(request):
    request.session.flush()  # پاک کردن تمام سشن‌ها
    return redirect('login')

def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # بررسی رمز عبور قبلی
        if check_password(old_password, user.password):
            # به‌روزرسانی اطلاعات کاربر
            user.username = username
            user.email = email
            if new_password:  # اگر رمز عبور جدید داده شده باشد
                user.password = make_password(new_password)  # هش کردن رمز عبور جدید
            user.save()

            return redirect('main')  # بازگشت به صفحه اصلی بعد از ذخیره تغییرات
        else:
            message = "رمز عبور قبلی اشتباه است."
            return render(request, 'users/EditProfile.html', {'user': user, 'message': message})

    return render(request, 'users/EditProfile.html', {'user': user})