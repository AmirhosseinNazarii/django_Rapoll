from django.shortcuts import render

def panel1(request):
    return render(request, 'adminpanel/panel1.html')
