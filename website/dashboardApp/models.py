from django.db import models

class Fruit(models.Model):
    name = models.CharField(max_length=255)
    amt = models.IntegerField()

    def __str__(self):
        return self.name