from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length = 255,blank=True)
    cat_image = models.ImageField(upload_to = 'photos/categories', blank=True)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
            
    def __str__(self):
        return self.category_name

# class MainCategory(models.Model):
#     main_category_name = models.CharField(max_length=100,unique=True)
#     slug               = models.SlugField(max_length=100,unique=True)
#     description        = models.TextField(blank=True)

#     class Meta:
#         verbose_name       = 'Maincategory'
#         verbose_name_plural= 'Maincategories'

#     def get_url(self):
#         return reverse('products_by_main_category',args=[self.slug])

#     def __str__(self):
#         return self.main_category_name