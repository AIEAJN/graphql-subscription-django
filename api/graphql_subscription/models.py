from django.db import models

# Create your models here.

class Manga(models.Model):
    name = models.CharField(max_length=255, default=None, blank=False)
    synopsis = models.CharField(max_length=255, default=None, blank=True)
    author = models.CharField(max_length=100, default=None, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'manga'
        unique_together = (("name", "author"),)
    