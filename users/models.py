from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)  # ستون Is_admin با مقدار پیش فرض 0 (کاربر عادی)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ستون Balance با مقدار پیش فرض 0

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


