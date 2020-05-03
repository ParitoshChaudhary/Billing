from django.db import models
from django.contrib.auth import get_user_model
from menu_app.models import Item

# Create your models here.
class Bills(models.Model):
    user = get_user_model()
    total_cost = models.CharField(max_length=10, null=True, default='0.0')
    cgst = models.IntegerField(null=True, default=0)
    sgst = models.IntegerField(null=True, default=0)
    generated_by = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    items = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    generated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.generated_by

    class Meta:
        verbose_name_plural = 'Bills'
