from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import uuid
# Create your models here.


class CustomUser(AbstractUser):
    fullname=models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    savings_amount = models.FloatField()
    current_amount = models.FloatField()
    
    
    def generate_unique_account_number(self):
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(14)])
            if not CustomUser.objects.filter(account_number=account_number).exists():
                return account_number
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_unique_account_number()
        super().save(*args, **kwargs)
        




class Transactions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=100)
    amount = models.FloatField()
    account_type = models.CharField(max_length=100)
    
    
    
    def __str__(self):
        return f"{self.user.username}' coins is {self.created_at}"