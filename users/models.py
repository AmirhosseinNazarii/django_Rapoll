from django.db import models




class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)  # ستون Is_admin با مقدار پیش فرض False (کاربر عادی)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ستون Balance با مقدار پیش فرض 0
    status = models.BooleanField(default=False)  # ستون Status با مقدار پیش فرض 0 (غیرفعال)

    def __str__(self):
        return self.username
    
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')  # ارتباط یک به یک با مدل User
    full_name = models.CharField(max_length=255)  # ستون FullName
    last_name = models.CharField(max_length=255)  # ستون LastName
    national_code = models.CharField(max_length=10)  # ستون NationalCode با محدودیت 10 رقم
    card_number = models.CharField(max_length=16)  # ستون CardNumber
    phone_number = models.CharField(max_length=15)  # ستون PhoneNumber
    email = models.EmailField()  # ستون Email
    national_card = models.ImageField(upload_to='national_cards/')  # ذخیره آدرس عکس کارت ملی

    def __str__(self):
        return self.user.username

class BlockActive(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='blocks_active')
    city = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    alley = models.CharField(max_length=100)
    block_number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Block {self.block_number} in {self.neighborhood}, {self.city}'
    
    # مدل جدید برای ذخیره اطلاعات خرید و فروش بلوک‌ها
class Transaction(models.Model):
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='transactions_selling')  # فروشنده
    buyer = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_buying')  # خریدار می‌تواند null باشد
    block = models.ForeignKey('users.BlockActive', on_delete=models.CASCADE, related_name='transactions')  # بلوک معامله شده
    price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت بلوک
    status = models.BooleanField(default=False)  # وضعیت معامله (False: باز، True: تکمیل‌شده)
    
    # اطلاعات بلوک برای دسترسی مستقیم به جزئیات
    city = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    alley = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ثبت معامله

    def __str__(self):
        return f'Transaction between {self.seller} and {self.buyer} for Block {self.block.block_number}'
