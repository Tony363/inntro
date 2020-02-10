from django import forms
from .models import Index


class Index_form(models.Model):
    stock = models.CharField(max_length=100)
    # checkbox = models.BooleanField(default=False)
    

    def __str__(self):
        return self.stock
