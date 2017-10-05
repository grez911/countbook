from django.db import models

class Operations(models.Model):
    description = models.CharField()

class Records(models.Model):
    date = models.DateField(auto_now_add=True)
    operation = models.ForeignKey(Operations)
