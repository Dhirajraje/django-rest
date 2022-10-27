from django.db import models
from datetime import datetime
# Create your models here.

class Sale(models.Model):
    id=models.AutoField(primary_key=True)
    client_id = models.CharField(max_length=68)
    client_name = models.CharField(max_length=68)
    sale_amount = models.FloatField()
    sales_person = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.utcnow)
    
    def __str__(cls):
        return f'entry id {cls.id} for client {cls.client_name} by {cls.sales_person}'


