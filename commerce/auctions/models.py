from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=10, blank=False, unique= True,primary_key=True)
    #email = models.CharField(max_length=64,blank=False)
    #password = models.CharField(max_length=64,blank=False)

    def __str__(self):
        return f"{self.username}, name : {self.first_name} {self.last_name}, email : {self.email}, password: {self.password} "

class Products(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=20,blank=False)
    prod_image = models.CharField(max_length=256,blank=True)
    seller_id = models.ForeignKey(User, on_delete= models.CASCADE, related_name="sellers_id")
    description = models.TextField(blank=False)
    amount = models.IntegerField()
    post_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return f"{self.prod_id}: prod_name:{self.prod_name}, prod_image:{self.prod_image}, seller_id :{self.seller_id},  description: {self.description}, amount: {self.amount}, post_date:{self.post_date}, end_date: {self.end_date},active: {self.active} "


class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_id")
    bid_date = models.DateField()
    min_amount = models.IntegerField()
    bid_amt = models.IntegerField()
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bidder_id")

    def __str__(self):
        return f"{self.bid_id}: prod_id {self.product_id}, bid_date: {self.bid_date}, min_amt: {self.min_amount}, bid_amt:{self.bid_amt}, bidder_id: {self.bidder_id}"


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    commenter_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter_name")
    message = models.TextField()
    prod_id = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="products_id")
    comment_date = models.DateField()

    def __str__(self):
        return f"{self.comment_id}: commenter_id:{self.commenter_id}, message:{self.message}, prod_id:{self.prod_id}, date:{self.comment_date}"
    
class WatchList(models.Model):
    list_id = models.AutoField(primary_key=True)
    prod_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.list_id}: prod_id:{self.prod_id}, user_id:{self.user_id}"
