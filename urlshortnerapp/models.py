from django.db import models

class URL(models.Model):
    original_url=models.URLField()
    shortened_url=models.CharField(max_length=10,unique=True)
    click_count=models.IntegerField(default=0)
    
    def __str__(self):
        return self.shortened_url