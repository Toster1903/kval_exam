from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    number_field = models.IntegerField(default=0)
    date_field = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
