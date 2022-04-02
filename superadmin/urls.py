from django.urls import path
from . import views



urlpatterns = [
    path('superadmin/',views.index_,name="superindex"),
    path('superadmin/users/',views.users_,name="super_users"),
    path('superadmin/user/<int:user_pk>/',views.login_user_account,name="super_users_log"),
    path('superadmin/withdrawals/',views._withdraws_,name="super_with"),
    path('superadmin/withdrawals/<int:with_pk>/',views.process_withdrawal,name="super_users_pro_with"),
    path('superadmin/deposits/',views._deposit_,name="super_deposit"),

    path('superadmin/deposits/<int:depo_pk>/',views.process_deposit,name="super_users_pro_depo"),

   path('superadmin/trades/',views._trades_,name="super_trades"),
   path('superadmin/ongoing-trades/',views.ongoin_trades,name="super_ongoin_trades"),

   path('superadmin/process-ongoing-trades/',views.edit_ongoin_trade,name="super_process_ongoin_trades"),
   path('superadmin/documents/',views.documents_,name="super_doc"),
   path('superadmin/process-document/',views.process_documents_,name="super_process_doc"),

]