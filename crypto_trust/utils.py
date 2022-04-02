from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from uuid import uuid4



EMAIL_ADMIN = settings.DEFAULT_FROM_EMAIL
D =  'deposite'
W = "withdraw"



def set_expirable_var(session, var_name, value, expire_at):
    session[var_name] = {'value': value, 'expire_at': expire_at.timestamp()}

def get_expirable_var(session, var_name, default=None):
    var = default
    if var_name in session:
        my_variable_dict = session.get(var_name, {})
        if my_variable_dict.get('expire_at', 0) > datetime.now().timestamp():
            var = my_variable_dict.get('value')
        else:
            del session[var_name]
    return var



def verify_exp():
    return timezone.now() + timedelta(minutes=10)

def reg_code():
    code = str(uuid4()).replace(" ","-").upper()[:6]
    return code

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip





def get_next_destination(request):
    next = None
    if request.GET.get('next'):
        next = str(request.GET.get('next'))
    return next





def check_trade(ongoingtrade,trade):
    bool_list = []
    for obj in ongoingtrade.objects.all():
        if trade.amount == obj.amount:
            bool_list.append(True)
            print("true")
        else:
            bool_list.append(False)
            print('False')
        if trade.sysmbol == obj.sysmbol:
            bool_list.append(True)
            print(True)
        else:
            bool_list.append(False)
            print(False)
        if trade.leverage == obj.leverage:
            bool_list.append(True)
            print(True)
        else:
            bool_list.append(False)
            print(False)
        if trade.interval == obj.interval:
            bool_list.append(True)
            print(True)
        else:
            bool_list.append(False)
            print(False)
    
    return all(bool_list)
