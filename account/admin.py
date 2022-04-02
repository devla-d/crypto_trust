from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Account,Referral



class UserAdmin(BaseUserAdmin):
 
  fieldsets = (
      (None, {'fields': ('email', 'password', )}),
      (_('Personal info'), {'fields': ('username','country','gender','zipcode','city','address','phone_number')}),
      (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_email_verifield' ,'ty_pe','is_verified')}),
      (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {'fields': ('ref_code','refferal', 'tot_balance','amount_withdraw','deposit_balance','deposit_method','ref_balance','tot_amount_invested')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('email', 'password1', 'password2'),
      }),
  )
  list_display = [ 'username','email' ]
  search_fields = ('email', 'username' )
  ordering = ('id', )



# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
admin.site.register(Referral)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)