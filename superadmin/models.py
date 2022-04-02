from django.db import models

# Create your models here.




class OngoingTrade(models.Model):
    amount = models.IntegerField( blank=True,null=True)
    sysmbol = models.CharField(max_length=50)
    interval = models.IntegerField(default=0)
    leverage = models.FloatField(default=0)
    pay = models.IntegerField( default=30,blank=True,null=True)



    def __str__(self):
        return f"{self.sysmbol}"