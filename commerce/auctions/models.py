from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    pass
class listings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    minimum_bid=models.DecimalField(max_digits=10,decimal_places=2)
    image_url=models.CharField(max_length=300)
    category=models.CharField(max_length=100)
    def __str__(self):
        return self.title
class bid(models.Model):
    current_bid=models.DecimalField(max_digits=10,decimal_places=2)
    item=models.ForeignKey(listings,on_delete=models.CASCADE)
    updatedby=models.CharField(max_length=200,default='default_value')
    num_of_updates=models.IntegerField(default=0)
class watchlist(models.Model):
    item=models.ForeignKey(listings,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
class comments(models.Model):
    comment=models.TextField()
    item=models.ForeignKey(listings,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)