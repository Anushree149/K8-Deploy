from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    desc=models.TextField(max_length=2000)
    image=models.ImageField(upload_to='photos/products')
    price=models.IntegerField()
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_by_product',args=[self.category.slug,self.slug])

variation_choices=(
        ('color','color'),
        ('size','size'),
         )
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)

class Variation(models.Model):
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     variation_category=models.CharField(max_length=100,choices=variation_choices)
     variation_value=models.CharField(max_length=100)
     is_active=models.BooleanField(default=True)
     created_date=models.DateTimeField(auto_now=True)

     objects=VariationManager()

     def __str__(self):
        return self.variation_value
