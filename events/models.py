from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField('Venue Address', max_length=300)
    zip_code = models.CharField('Venue Zip Code', max_length=15)
    phone = models.CharField('Phone Contact', max_length=25)
    web = models.URLField('WebPage', blank=True)
    email = models.EmailField('EmailAddress', blank=True)
    owner = models.ForeignKey(User, related_name='owner', blank=False, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True, upload_to="images/venues")
    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='manager', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(User, related_name='attendees', blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/events")

    def __str__(self):
        return self.name