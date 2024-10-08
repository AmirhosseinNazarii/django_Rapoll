from django.db import models
from users.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'در حال بررسی'),
        ('answered', 'پاسخ داده شد'),
        ('closed', 'بسته شد'),
    ]

    ticket_id = models.AutoField(primary_key=True)  # شماره تیکت
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # کاربری که تیکت ارسال کرده
    subject = models.CharField(max_length=100)  # موضوع تیکت
    message = models.TextField(max_length=500)  # متن تیکت
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')  # وضعیت تیکت
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد تیکت
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ آخرین به‌روزرسانی
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)  # فایل پیوست شده

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.subject}"

