from django.db import models
from category.models import Category
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_length=10,decimal_places=5,max_digits=10)
    image_url=models.URLField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()


    def __str__(self):
        return self.name