from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SignUpForm
from django.contrib.auth.hashers import make_password
from adminpanel.models import Block
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from adminpanel.models import Block
from .models import User, BlockActive



def buy_block(request):
    if request.method == 'POST':
        block_id = request.POST['block_id']
        block_number = request.POST['block_number']
        price = float(request.POST['price'])
        user = User.objects.get(id=request.session['user_id'])
        
        # ارسال اطلاعات به صفحه خرید
        return render(request, 'users/BuyBlock.html', {
            'block_id': block_id,
            'block_number': block_number,
            'price': price,
            'user': user
        })

def finalize_purchase(request):
    if request.method == 'POST':
        block_id = request.POST['block_id']
        price = float(request.POST['price'])
        user = User.objects.get(id=request.session['user_id'])

        # بررسی موجودی کاربر
        if user.balance >= price:
            # کسر موجودی کاربر
            user.balance -= price
            user.save()

            # ذخیره اطلاعات بلوک خریداری شده
            BlockActive.objects.create(
                user=user,
                block_number=request.POST['block_number'],
                price=price,
                city='تهران',  # برای سادگی، می‌توانید اطلاعات دقیق‌تر اضافه کنید
                neighborhood='محله',
                street='خیابان',
                alley='کوچه'
            )
            messages.success(request, 'خرید بلوک با موفقیت انجام شد!')
            return redirect('main')
        else:
            messages.error(request, 'موجودی حساب شما کافی نیست، لطفاً حساب خود را شارژ کنید.')
            return redirect('buy_block')

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
    
def block_search(request):
    city = request.GET.get('city', '')
    neighborhood = request.GET.get('neighborhood', '')
    street = request.GET.get('street', '')
    alley = request.GET.get('alley', '')

    blocks = Block.objects.all()

    if city:
        blocks = blocks.filter(city=city)
    if neighborhood:
        blocks = blocks.filter(neighborhood=neighborhood)
    if street:
        blocks = blocks.filter(street=street)
    if alley:
        blocks = blocks.filter(alley=alley)

    return render(request, 'users/main.html', {
        'blocks': blocks,
        'selected_city': city,
        'selected_neighborhood': neighborhood,
        'selected_street': street,
        'selected_alley': alley
    })


def get_neighborhoods(request):
    city = request.GET.get('city')
    neighborhoods = Block.objects.filter(city=city).values_list('neighborhood', flat=True).distinct()
    return JsonResponse(list(neighborhoods), safe=False)

def get_streets(request):
    city = request.GET.get('city')
    neighborhood = request.GET.get('neighborhood')
    streets = Block.objects.filter(city=city, neighborhood=neighborhood).values_list('street', flat=True).distinct()
    return JsonResponse(list(streets), safe=False)

def get_alleys(request):
    city = request.GET.get('city')
    neighborhood = request.GET.get('neighborhood')
    street = request.GET.get('street')
    alleys = Block.objects.filter(city=city, neighborhood=neighborhood, street=street).values_list('alley', flat=True).distinct()
    return JsonResponse(list(alleys), safe=False)

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

def search_blocks(request):
    city = request.GET.get('city')
    neighborhood = request.GET.get('neighborhood')
    street = request.GET.get('street')
    alley = request.GET.get('alley')

    blocks = Block.objects.filter(
        city=city,
        neighborhood=neighborhood,
        street=street,
        alley=alley
    )

    # داده‌های بلوک‌ها را به صورت JSON برمی‌گردانیم
    block_data = [
        {
            'id':block.id,
            'block_number': block.block_number,
            'price': block.price,
            'status': block.status
        }
        for block in blocks
    ]
    
    return JsonResponse(block_data, safe=False)