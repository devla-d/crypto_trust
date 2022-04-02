from django.urls import path

from . import views

urlpatterns = [
    path('index/',views.index_,name='dashboard'),
    path('trading-history/',views.trading_history_,name='trading_history'),
    path('withdraw-funds/',views.withdraw_,name='withdraw'),
    path('verify-account/',views.verification_,name='verification'),
    path('financial-transactions/',views.transactions_,name='transactions'),
    path('my-account/',views.account_,name='account'),
    path('deposite-funds/',views.deposit_,name='deposit'),
    path('process-deposit/',views.process_deposit,name='proc-deposit'),
    path('trade/',views.trade_,name='trade'),
    path('notifications/',views.notification_,name="notify"),

    path('process-trade/',views.process_trade,name="process_trade_"),

]