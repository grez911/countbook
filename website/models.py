from django.db import models

class Operation(models.Model):
    name = models.TextField()
    show = models.BooleanField()

class Record(models.Model):
    date = models.DateField(auto_now_add=True)
    operation = models.ForeignKey(Operation)
