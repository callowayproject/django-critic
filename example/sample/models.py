from django.db import models

class Sample(models.Model):
    name = models.TextField()
    something = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name
        
class Product(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    
    def __unicode__(self):
        return self.name