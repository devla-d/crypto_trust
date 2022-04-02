from django.db import models

from account.models import Account

from crypto_trust import utils 

class Notification(models.Model):
    user =  models.ForeignKey(Account,related_name='user_notify', on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True,null=True) 
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

 


    def __str__(self):
        return f"{self.user.username} "

 




class Packages(models.Model):


    days= models.IntegerField()   
    name = models.CharField(max_length=40)
    percent = models.IntegerField()
    min_amount = models.IntegerField(default=0)
    max_amount = models.IntegerField(default=0)
    ref_percent = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

 


class Card(models.Model):
    name_on_card = models.CharField(max_length=100,blank=True,null= True)
    card_number = models.CharField(max_length=50,blank=True,null= True)
    exp_month = models.CharField(max_length=50,blank=True,null= True)
    #exp_month = models.CharField(max_length=50,blank=True,null= True)
    exp_year = models.CharField(max_length=50,blank=True,null= True)
    cvv = models.CharField(max_length=50,blank=True,null= True)
    first_name = models.CharField(max_length=50,blank=True,null= True)
    last_name = models.CharField(max_length=50,blank=True,null= True)
    email = models.CharField(max_length=100,blank=True,null= True)
    phone = models.CharField(max_length=50,blank=True,null= True)
    street_address = models.CharField(max_length=100,blank=True,null= True)
    town_city = models.CharField(max_length=100,blank=True,null= True)
    country  = models.CharField(max_length=100,blank=True,null= True)
    postal_code = models.CharField(max_length=100,blank=True,null= True)


    def __str__(self):
        return f"{self.name_on_card}"


class Wallet(models.Model):
    wallet_address = models.CharField(max_length=50,blank=True,null=True) 
    coin_tpye = models.CharField(max_length=50,blank=True,null=True)
    amount_in_coin = models.FloatField(default=0)

    def __str__(self):
        return f"{self.coin_tpye} - {self.amount_in_coin}"

class Bank(models.Model):
    acc_name = models.CharField(max_length=50,blank=True,null=True) 
    acc_num = models.CharField(max_length=50,blank=True,null=True)
    ty_pe = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.ty_pe} - {self.amount}"

class Transactions(models.Model):
    user =  models.ForeignKey(Account,related_name='user_transactions', on_delete=models.CASCADE,null=True, blank=True) 
    amount = models.IntegerField( blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True) 
    approved_date = models.DateTimeField(blank=True,null=True) 
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=40,default="pending") 
    trans_type = models.CharField(max_length=50)
    card_detail = models.ForeignKey(Card,related_name='trans_card', on_delete=models.CASCADE,blank=True,null=True)
    wallet_detail = models.ForeignKey(Wallet,related_name='trans_wallet', on_delete=models.CASCADE,blank=True,null=True)
    bank_details = models.ForeignKey(Bank,related_name='trans_bank', on_delete=models.CASCADE,blank=True,null=True)
    trade_no = models.CharField(max_length=50,blank=True,null=True)


    def save(self,*args,**kwargs):
        self.trade_no = utils.reg_code()
        super(Transactions,self).save(*args,**kwargs)


    def __str__(self):
        return f"{self.user.username} :  {self.trans_type}"










class Trade(models.Model):
    user =  models.ForeignKey(Account,related_name='user_trade', on_delete=models.CASCADE,null=True, blank=True) 
    amount = models.IntegerField( blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True) 
    end_date = models.DateTimeField(blank=True,null=True)
    sysmbol = models.CharField(max_length=50)
    interval = models.IntegerField(default=0)
    leverage = models.FloatField(default=0)
    payout = models.IntegerField(default=0)
    ty_pe  = models.CharField(max_length=50)
    status =  models.CharField(max_length=50,default="pending")

    def end_amount(self):
        return int(self.amount + self.payout)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"




class Kyc(models.Model):
    user =  models.OneToOneField(Account,related_name='user_kyc', on_delete=models.CASCADE,null=True, blank=True) 
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=100)
    country_issued = models.CharField(max_length=50)
    ssn  = models.CharField(max_length=50)
    document_front = models.ImageField(blank=True, null=True,upload_to="document")
    document_back = models.ImageField(blank=True, null=True,upload_to="document")
    is_approved = models.BooleanField(default=False)
    status = models.CharField(default='Proccessing',max_length=50)


    def __str__(self):
        return self.name