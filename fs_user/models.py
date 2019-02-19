from django.db import models


class UserInfo(models.Model):
    u_name = models.CharField(max_length=20)
    u_password = models.CharField(max_length=200)
    u_email = models.CharField(max_length=60)
    u_shou_address = models.CharField(max_length=200)
    u_postcode = models.CharField(max_length=6)
    u_phone = models.CharField(max_length=11)

