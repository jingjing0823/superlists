from django.db import models

# Create your models here.

class UserOrder(models.Model):
    orderno=models.CharField(max_length=200)
    mobile=models.CharField(max_length=20)
    status_code=models.CharField(max_length=20)
    status=models.CharField(max_length=50)
    issorderno=models.CharField(max_length=200)
    iss_mobile=models.CharField(max_length=20,null=True)
    iss_name=models.CharField(max_length=20,null=True)
    
    class Meta:
        db_table="user_order"
    