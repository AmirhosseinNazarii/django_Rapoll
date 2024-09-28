from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.hashers import make_password

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

