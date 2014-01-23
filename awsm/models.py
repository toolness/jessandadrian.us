from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Place(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    place = models.ForeignKey(Place)
    categories = models.ManyToManyField(Category)
    start = models.DateTimeField()
    duration = models.TimeField()
