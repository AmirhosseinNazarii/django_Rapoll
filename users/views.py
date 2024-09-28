from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import check_password
from django.contrib import messages
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
                return redirect('main')  # انتقال به صفحه اصلی
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
