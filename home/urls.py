from django.urls import path

from .  import  views



urlpatterns = [
    path('',views.index,name='home'),
    path('about-us/',views.about_us,name='about-us'),
    path('asset/',views.asset,name="assets_"),
    path('pricing/',views.pricing,name="pricing_"),
    path('faqs/',views.faqs,name="faqs_"),
    path('help-center/',views.help_center,name="help_center_"),

]
