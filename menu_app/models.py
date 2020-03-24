from django.db import models


# Create your models here.
class Cuisine(models.Model):
    cuisine = models.CharField(max_length=15)

    def __str__(self):
        return self.cuisine

    class Meta:
        verbose_name_plural = 'cuisines'


class Category(models.Model):
    category_type = models.CharField(max_length=9)

    def __str__(self):
        return self.category_type

    class Meta:
        verbose_name_plural = 'category type'


class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
