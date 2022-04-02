from django.db import models
from django.contrib.auth.models import AbstractUser



#Admin pass = testww23



class Account(AbstractUser):
    email       = models.EmailField(verbose_name='email', max_length=60, unique=True )
    phone_number = models.CharField(max_length=14,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    is_email_verifield = models.BooleanField(default=False)
    fullname = models.CharField(max_length=80,blank=True,null= True)
    city = models.CharField(max_length=50,blank=True,null= True)
    country = models.CharField(max_length=50,blank=True,null= True)
    gender = models.CharField(max_length=10,blank=True,null=True)
    zipcode = models.CharField(max_length=10, blank=True,null= True)
    address = models.CharField(max_length=100,blank=True,null= True)
    ref_code = models.CharField(max_length=100,blank=True,null= True)
    refferal = models.IntegerField(default=0)
    deposit_method = models.CharField(max_length=50,blank=True,null= True)
    deposit_balance = models.IntegerField(default=0)

    tot_balance = models.IntegerField(default=0)
    ref_balance = models.IntegerField(default=0)
    amount_withdraw = models.IntegerField(default=0)
    tot_amount_invested = models.IntegerField(default=0)

    ty_pe = models.CharField(max_length=50,blank=True,null= True)


    REQUIRED_FIELDS = ['phone_number','fullname','email']


    def __str__(self):
        return self.username




class Referral(models.Model):
    user = models.OneToOneField(Account, on_delete = models.CASCADE)
    recommended_by = models.ForeignKey(Account,related_name='recom_user', on_delete=models.CASCADE,null=True, blank=True)
    recomended_users = models.ManyToManyField(Account, related_name='my_referrals',blank=True)
    date = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return self.user.username
