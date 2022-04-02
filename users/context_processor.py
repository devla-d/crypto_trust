from django.conf import settings
#from django.utils import timezone
#from datetime import  timedelta
from .models import Notification,Kyc



def user_processor(request):
    user = request.user
    if user.is_authenticated:
        user_notify_count = Notification.objects.filter(user=request.user,read=False).count()
        try:
            doc = Kyc.objects.get(user=request.user)
        except Kyc.DoesNotExist:
            doc = None
            
            euro_country = ["Malta","Luxembourg","Cyprus","Estonia","Latvia","Slovenia","Lithuania","Ireland","Slovakia","Finland","Austria","Greece","Portugal","Belgium","Netherlands","Spain","Italy","France","Germany"]
            rand_country = ["South Africa"]
            if user.country in euro_country:
                currency = "€"
                sysm = "EUR"
            elif user.country in rand_country:
                currency = "R"
                sysm = "ZAR"
            elif user.country == "United Kindom":
                currency = "£"
                sysm = "GBP"
            else:
                currency = "$"
                sysm = "USD"
            return {"user_notify_count":user_notify_count,'doc':doc,"currency":currency,"sysm":sysm}
    else:
        return {"user_notify": 0}




