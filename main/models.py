from django.db import models

# Create your models here.

class district_tb(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=255)
    district_img = models.URLField(max_length=255)
    district_desc = models.TextField()

    def __str__(self):
        return self.district_name
