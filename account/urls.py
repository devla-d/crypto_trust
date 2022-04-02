from django.urls import path


from . import views



urlpatterns = [
    path('login/',views.login_,name="login"),
    path('get-started/',views.register_,name="register"),
    path('verify-email/',views.confirm_email,name="confirm-email"),
     path('logout/',views.logout_,name="logout"),
]