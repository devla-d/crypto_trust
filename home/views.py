from django.shortcuts import render,redirect,get_object_or_404
from django.http import  HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta



from crypto_trust import utils




def index(request):
    print(utils.get_client_ip(request))
    return render(request,'home/index.html')



def about_us(request):
    return render(request,'home/about-us.html')


def asset(request):
    return render(request,'home/assets.html')



def pricing(request):
    return render(request,'home/pricing.html')




def faqs(request):
    return render(request,'home/faqs.html')



def help_center(request):
    return render(request,"home/help.html")