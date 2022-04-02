from django.contrib import admin


from .models import Transactions,Notification,Card,Wallet,Trade,Bank,Kyc


admin.site.register(Transactions)
admin.site.register(Notification)
admin.site.register(Card)
admin.site.register(Wallet)
admin.site.register(Trade)
admin.site.register(Bank)
admin.site.register(Kyc)