from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class Cuisine(models.Model):
    cuisine = models.CharField(max_length=15)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        value = str(self.cuisine) + ' - ' + str(self.added_by)
        return self.cuisine

    class Meta:
        verbose_name_plural = 'cuisines'


class Category(models.Model):
    category_type = models.CharField(max_length=9)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        value = str(self.category_type) + ' - ' + str(self.added_by)
        return self.category_type

    class Meta:
        verbose_name_plural = 'category type'


class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)

    def __str__(self):
        value = str(self.name) + ' - ' + str(self.added_by)
        return self.name
