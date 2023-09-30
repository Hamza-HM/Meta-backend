from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    inventory = models.IntegerField(null=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['price'])
        ]

    def __str__(self):
        return str(self.title)
    
class Category(models.Model):
    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=100)
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    inventory = models.IntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    
    class Meta:
        indexes = [
            models.Index(fields=['price'])
        ]

    def __str__(self):
        return str(self.title)
    
