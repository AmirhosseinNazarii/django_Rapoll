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
from decimal import Decimal
from .models import Transaction
from .models import BlockActive
from django.db.models import Q
from .models import Ticket, TicketMessage
from django.core.files.storage import FileSystemStorage




def buy_block(request):
    if request.method == 'POST':
        block_id = request.POST['block_id']
        block_number = request.POST['block_number']
        price = float(request.POST['price'])
        city = request.POST['city']
        neighborhood = request.POST['neighborhood']
        street = request.POST['street']
        alley = request.POST['alley']
        user = User.objects.get(id=request.session['user_id'])
        
        # ارسال اطلاعات به صفحه خرید
        return render(request, 'users/BuyBlock.html', {
            'block_id': block_id,
            'block_number': block_number,
            'price': price,
            'city': city,
            'neighborhood': neighborhood,
            'street': street,
            'alley': alley,
            'user': user
        })


def finalize_purchase(request):
    if request.method == 'POST':
        block_id = request.POST['block_id']
        block_number = request.POST['block_number']
        price = Decimal(request.POST['price'])  # تبدیل price به Decimal
        city = request.POST['city']
        neighborhood = request.POST['neighborhood']
        street = request.POST['street']
        alley = request.POST['alley']
        user = User.objects.get(id=request.session['user_id'])

        # تبدیل موجودی کاربر به Decimal
        user.balance = Decimal(user.balance)

        # بررسی موجودی کاربر
        if user.balance >= price:
            # کسر موجودی کاربر
            user.balance -= price
            user.save()

            # ذخیره اطلاعات بلوک خریداری شده
            block_active = BlockActive.objects.create(
                user=user,
                block_number=block_number,
                price=price,
                city=city,
                neighborhood=neighborhood,
                street=street,
                alley=alley
            )

            # تغییر وضعیت بلوک به فروخته شده
            try:
                block = Block.objects.get(id=block_id)
                block.status = True  # تغییر وضعیت به True (فروخته شده)
                block.save()
            except Block.DoesNotExist:
                messages.error(request, 'بلوک یافت نشد.')

            # انتقال کاربر به صفحه BuySuccess
            return render(request, 'users/BuySuccess.html', {
    'block_number': block_number,
    'price': price,
    'user': user,
    'city': city,
    'neighborhood': neighborhood,
    'street': street,
    'alley': alley
})
        else:
            # انتقال کاربر به صفحه BuyFailed
            return render(request, 'users/BuyFailed.html')
        

        
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
            'neighborhood':block.neighborhood,
            'street':block.street,
            'alley':block.alley,
            'city':block.city,
            'id':block.id,
            'block_number': block.block_number,
            'price': block.price,
            'status': block.status
        }
        for block in blocks
    ]
    
    return JsonResponse(block_data, safe=False)

def buylist(request):
    user_id = request.session.get('user_id')  # گرفتن user_id از session
    if user_id:
        user = User.objects.get(id=user_id)
        purchases = BlockActive.objects.filter(user=user)  # فیلتر کردن خریدها بر اساس user_id

        return render(request, 'users/buylist.html', {'purchases': purchases})
    else:
        return redirect('login')
    
def sell_block(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)
    blocks = BlockActive.objects.filter(user=user)  # بلوک‌های کاربر

    # اضافه کردن اطلاعات اضافی به هر بلوک برای نمایش در صفحه
    for block in blocks:
        block.is_listed = Transaction.objects.filter(block=block, status=False).exists()  # آیا آگهی شده؟
        block.max_price = block.price * Decimal('1.22')  # حداکثر قیمت مجاز

    return render(request, 'users/sellblock.html', {'blocks': blocks})

def list_block(request, block_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        block = BlockActive.objects.get(id=block_id)
        user = User.objects.get(id=user_id)

        # بررسی اینکه بلوک قبلاً آگهی نشده باشد
        existing_transaction = Transaction.objects.filter(block=block, status=False).exists()
        if existing_transaction:
            messages.error(request, 'شما قبلا این بلوک را آگهی کرده‌اید.')
            return redirect('sellblock')

        price = Decimal(request.POST.get('price'))
        max_price = block.price * Decimal('1.22')

        # بررسی محدودیت قیمت
        if price > max_price:
            messages.error(request, f'قیمت نباید بیشتر از {max_price} تومان باشد.')
            return redirect('sellblock')

        # ثبت آگهی جدید
        Transaction.objects.create(
            seller=user,
            block=block,
            price=price,
            city=block.city,
            neighborhood=block.neighborhood,
            street=block.street,
            alley=block.alley
        )

        messages.success(request, 'آگهی شما با موفقیت ثبت شد.')
        return redirect('sellblock')
    
def buy_from_user(request):
    city = request.GET.get('city')
    neighborhood = request.GET.get('neighborhood')
    street = request.GET.get('street')
    alley = request.GET.get('alley')

    # فیلتر کردن تراکنش‌هایی که وضعیتشان False است (باز)
    transactions = Transaction.objects.filter(status=False)

    if city:
        transactions = transactions.filter(city=city)
    if neighborhood:
        transactions = transactions.filter(neighborhood=neighborhood)
    if street:
        transactions = transactions.filter(street=street)
    if alley:
        transactions = transactions.filter(alley=alley)

    return render(request, 'users/BuyFromUser.html', {
        'transactions': transactions,
        'cities': Transaction.objects.values_list('city', flat=True).distinct()  # لیست شهرها برای فیلتر
    })

def final_buy_from_user(request):
    if request.method == 'POST':
        transaction_id = request.POST['transaction_id']
        user = User.objects.get(id=request.session['user_id'])  # دریافت کاربر لاگین شده (خریدار)
        transaction = Transaction.objects.get(id=transaction_id)

        # بررسی اینکه خریدار و فروشنده یکی نباشند
        if transaction.seller == user:
            # هدایت به صفحه خطا و نمایش پیام
            return render(request, 'users/FinalBuyFromUser.html', {
                'error': True,
                'message': "شما نمیتوانید بلوکی که خودتان مالک آن هستید رو خریداری کنید!"
            })

        # تبدیل موجودی خریدار به Decimal
        user.balance = Decimal(user.balance)
        block_price = Decimal(transaction.price)

        # بررسی موجودی کاربر
        if user.balance >= block_price:
            # کسر موجودی از خریدار
            user.balance -= block_price
            user.save()

            # اضافه کردن موجودی به فروشنده
            seller = transaction.seller
            seller.balance = Decimal(seller.balance) + block_price
            seller.save()

            # آپدیت مالکیت بلوک
            block = transaction.block
            block.user = user  # انتقال مالکیت به خریدار جدید
            block.price = block_price  # آپدیت قیمت جدید
            block.save()

            # آپدیت وضعیت تراکنش
            transaction.status = True  # معامله نهایی شده
            transaction.buyer = user  # ثبت خریدار
            transaction.save()

            # هدایت به صفحه FinalBuyFromUser.html با نمایش فاکتور
            return render(request, 'users/FinalBuyFromUser.html', {
                'block': block,
                'transaction': transaction,
                'success': True  # خرید موفقیت آمیز
            })
        else:
            # اگر موجودی کافی نبود
            return render(request, 'users/FinalBuyFromUser.html', {
                'block': transaction.block,
                'transaction': transaction,
                'insufficient_funds': True  # پیام عدم موجودی کافی
            })

    # اگر به هر دلیل دیگری معامله انجام نشد (به طور پیش‌فرض)
    return render(request, 'users/FinalBuyFromUser.html', {
        'error': True  # پیام خطا در عملیات
    })

    
def support(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    tickets = Ticket.objects.filter(user=user)  # تیکت‌های کاربر

    return render(request, 'users/support.html', {'tickets': tickets})

def send_ticket(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)

        subject = request.POST.get('subject')
        message = request.POST.get('message')
        file = request.FILES.get('file')

        # ذخیره تیکت
        ticket_number = Ticket.objects.count() + 10001  # شماره تیکت از 10001 شروع می‌شود
        ticket = Ticket.objects.create(user=user, subject=subject, ticket_number=ticket_number)
        
        # ذخیره پیام
        if file:
            fs = FileSystemStorage()
            file_name = fs.save(file.name, file)
            TicketMessage.objects.create(ticket=ticket, user=user, message=message, file=file_name)
        else:
            TicketMessage.objects.create(ticket=ticket, user=user, message=message)

        return redirect('support')  # به صفحه پشتیبانی برگردید

    return render(request, 'users/send_ticket.html')

def send_ticket_detail(request, ticket_number):
    ticket = Ticket.objects.get(ticket_number=ticket_number)
    messages = TicketMessage.objects.filter(ticket=ticket)

    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        message = request.POST.get('message')

        TicketMessage.objects.create(ticket=ticket, user=user, message=message)

    return render(request, 'users/send_ticket_detail.html', {'ticket': ticket, 'messages': messages})

def close_ticket(request, ticket_number):
    ticket = Ticket.objects.get(ticket_number=ticket_number)
    ticket.status = 'بسته شده'
    ticket.save()
    return redirect('admin_support')  # به صفحه مدیریت تیکت‌ها برگردید


def block_search_id(request):
    if request.method == 'GET':
        block_id = request.GET.get('block_id')  # دریافت مقدار ورودی کاربر
        
        if block_id:
            try:
                # فیلتر کردن بلوک‌ها بر اساس id
                block = Block.objects.get(id=block_id)
                
                # ارسال اطلاعات بلوک در قالب JSON
                return JsonResponse({
                    'status': 'success',
                    'block': {
                        'id': block.id,  # اضافه کردن id به اینجا
                        'city': block.city,
                        'neighborhood': block.neighborhood,
                        'street': block.street,
                        'alley': block.alley,
                        'block_number': block.block_number,
                        'price': block.price,
                        'status': 1 if block.status else 0,  # مقدار status را به صورت عددی (0 یا 1) برمی‌گردانیم
                    }
                })
            except Block.DoesNotExist:
                # اگر بلوکی با شناسه وارد شده یافت نشد
                return JsonResponse({'status': 'error', 'message': 'بلوک یافت نشد.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'شناسه وارد نشده است.'})
