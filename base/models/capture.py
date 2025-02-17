from django.db import models
from .item import Item, Format, create_id
import os

def upload_data_to(instance, filename):
    name = instance.item.name.replace(' ','')
    format = instance.format.name.replace(' ','')
    return os.path.join('downloads','capture', name, format, filename)

class Capture(models.Model):
    id = models.CharField(default=create_id, primary_key=True,
                          max_length=32, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, blank=False)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, null=False, blank=False)
    data = models.FileField(upload_to=upload_data_to)

    def __str__(self):
        return self.data.url