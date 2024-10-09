from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Ticket
from users.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

def support(request):
    user = get_object_or_404(User, id=request.session.get('user_id'))
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'support/support.html', {'tickets': tickets})

def send_ticket(request):
    user = get_object_or_404(User, id=request.session.get('user_id'))
    
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        attachment = request.FILES.get('attachment')
        
        if len(message) > 500:
            messages.error(request, 'طول پیام نباید بیش از 500 کاراکتر باشد.')
            return redirect('send_ticket')
        
        # ذخیره فایل پیوست
        if attachment:
            if attachment.size > 1024 * 1024:
                messages.error(request, 'حجم فایل نباید بیش از 1 مگابایت باشد.')
                return redirect('send_ticket')
            fs = FileSystemStorage()
            filename = fs.save(attachment.name, attachment)
        else:
            filename = None
        
        # ساخت تیکت
        Ticket.objects.create(
            user=user,
            subject=subject,
            message=message,
            attachment=filename
        )
        return redirect('support')
    
    return render(request, 'support/SendTicket.html')

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    return render(request, 'support/ticket_detail.html', {'ticket': ticket})

def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    ticket.status = 'closed'
    ticket.save()
    return redirect('support')

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)

    if request.method == 'POST':
        # دریافت پیام جدید
        message = request.POST['message']
        attachment = request.FILES.get('attachment')

        # بررسی طول پیام
        if len(message) > 500:
            messages.error(request, 'طول پیام نباید بیش از 500 کاراکتر باشد.')
            return redirect('ticket_detail', ticket_id=ticket_id)

        # بررسی فایل پیوست
        if attachment:
            if attachment.size > 1024 * 1024:
                messages.error(request, 'حجم فایل نباید بیش از 1 مگابایت باشد.')
                return redirect('ticket_detail', ticket_id=ticket_id)
            fs = FileSystemStorage()
            filename = fs.save(attachment.name, attachment)
        else:
            filename = None

        # ذخیره پیام جدید (اینجا می‌توانید مدلی برای ذخیره پیام‌های جدید اضافه کنید)
        # Message.objects.create(ticket=ticket, user=request.user, content=message, attachment=filename)

        messages.success(request, 'پیام شما با موفقیت ارسال شد.')
        return redirect('ticket_detail', ticket_id=ticket_id)

    return render(request, 'support/ticket_detail.html', {'ticket': ticket})

