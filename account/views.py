from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta,datetime

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template


from crypto_trust import utils
from account.models import Account,Referral
from .forms import RegForm,LoginForm



def login_(request):
    destination = utils.get_next_destination(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                if destination:
                    messages.info(request, "Login SuccessFul")
                    return redirect(destination)
                else:
                    messages.info(request, "Login SuccessFul")
                    return redirect('dashboard')
        else:
            messages.info(request,'INVALID CREDENTIALS')
    else:
        form = LoginForm()
    return render(request,'auth/login.html',{"form":form})



def logout_(request):
    logout(request)
    messages.info(request,"Logout Successfull")
    return redirect('login')

def register_(request):
    if request.POST:
        form = RegForm(request.POST)
        print(utils.reg_code())
        if form.is_valid():
            #instance = form.save()
            refferd_by_pk = request.POST.get('refferd_by')
            user = form.cleaned_data
            print(user['email'])
            if refferd_by_pk:
                user['is_reffered'] = True
                user['reffered_by_code'] = refferd_by_pk
            else:
                user['is_reffered'] = False
            user['ref_code'] = utils.reg_code()
            user['verify_code'] = utils.reg_code()
            user['verify_exp'] = str(timezone.now()+timedelta(minutes=10))
            #request.session['user'] = user
            #request.session.set_expiry
            expire_at = datetime.today() + timedelta(minutes=5)
            utils.set_expirable_var(request.session,'user',user,expire_at)
            subject = '[CRYPTOTRUSTRADE]Confirm Your Email Address'
            message = get_template("auth/account_activation_email.html").render(user)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[user['email']],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            messages.info(request,"Account Created Please Verify your Email Address")
            return redirect('confirm-email')
    else:
        form = RegForm()
    if request.GET.get('ref-code'):
        refferd_by = request.GET.get('ref-code')
        return render(request, 'auth/register.html',{"form":form , "refferd_by" : refferd_by})
    else:
        return render(request, 'auth/register.html',{"form":form})




def confirm_email(request):
    user = utils.get_expirable_var(request.session, 'user', None)
    if request.POST:
        code = request.POST.get('code')   
        if user:
            if code == user['verify_code']:
                new_user = Account(
                        username=user['username'],email=user['email'],
                        phone_number=user['phone_number'],fullname=user['fullname'],
                        ref_code=user['ref_code']
                    )
                new_user.set_password(user['password1'])
                new_user.save()

                if user['is_reffered'] == True:
                    try:
                        #Get The User That refferd the New User
                        refferd_by = Account.objects.get(ref_code=user['reffered_by_code'])
                        #Get The new user Referral Model
                        new_user_ref_m = Referral.objects.get(user =new_user)
                        #Asign refferd_by to new user and save
                        new_user_ref_m.recommended_by = refferd_by
                        #new_user_ref_m.user.ref_balance = 10
                        new_user_ref_m.user.save()
                        new_user_ref_m.save()
                        #Get The Old user Referral Model
                        refferd_by_ref_m = Referral.objects.get(user =refferd_by)
                        #add new user to old-user recom ref model
                        refferd_by_ref_m.recomended_users.add(new_user)
                        #increase old user referral  , bonus  and save
                        refferd_by_ref_m.user.refferal += 1
                        refferd_by_ref_m.user.ref_balance += 10
                        refferd_by_ref_m.user.tot_balance += 10
                        refferd_by_ref_m.user.save()
                        refferd_by_ref_m.save()
                    except:
                        messages.info(request, f'Something went Wrong')
                        del request.session['user']
                        return redirect('register')
                del request.session['user']
                messages.info(request,"Account Verified You Can now Login")
                return redirect('login')
            else:
                messages.info(request,'Invalid Code')
                return redirect('confirm-email')

        else:
            message.info(request,"UNKNOWN ERROR OCCURED")
            return redirect('register')
    if user:
        return render(request,'auth/confirm-email.html')
    else:
        return redirect('register')