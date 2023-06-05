from django.db import models
# from django.db.models.base import Model
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True,blank=True)
    description=models.TextField(max_length=2000,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name="category"
        verbose_name_plural="categories"
    
    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
        


