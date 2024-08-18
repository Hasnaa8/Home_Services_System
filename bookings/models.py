from django.db import models
from django.contrib.auth.models import User
from users.models import *
from services.models import *
# Create your models here.
class Booking(models.Model):
    customer = models.ForeignKey(Profile, related_name='customer_booking', on_delete=models.CASCADE, null=True)
    customer_username = models.CharField(max_length=200, null=True)
    customer_fname = models.CharField(max_length=200, null=True)
    customer_lname = models.CharField(max_length=200, null=True)
    
    
    provider = models.ForeignKey(Profile, related_name='provider_booking', on_delete=models.CASCADE, null=True)
    provider_username = models.CharField(max_length=200, null=True)
    
    service = models.ForeignKey(Service, related_name='service_booking', on_delete=models.CASCADE, null=True)
    service_category = models.CharField(max_length=50, null=True)
    
    STATUS = [
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
        ('completed', 'completed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS, default='pending')

    city_choices = (
            ('Homs', 'Homs'),
        )
    city = models.CharField(max_length=50, choices=city_choices, default='Homs')
    
    su_choices = (
        ('AlGhoota', 'AlGhoota'),
        ('AlHamra', 'AlHamra'),
        ('AlWa3r', 'AlWa3r'),
        ('Alinshaat', 'Alinshaat'),
        ('Alhadara','Alhadara'),
    )
    
    home_address = models.CharField(max_length=50, choices=su_choices, null=True)
    phone = models.CharField(max_length=50,null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    class Meta:
        verbose_name = 'Booking'

    def __str__(self):
        return f"Booking by {self.customer} with {self.provider} on {self.date} at {self.time} in {self.city}/{self.home_address}"
