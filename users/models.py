from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    USER = 1
    SUPERVISOR = 2
    ROLES = (
        (USER, 'user'),
        (SUPERVISOR, 'Supervisor'),
    )

    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='photos/%y/%m/%d',null=True)
    bdate = models.DateField(null=True)

    GENDER_CHOICES = (
        ('male','male'),
        ('female','female'),
        )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    
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
    
    phone = models.CharField(max_length=50)
    
    
    is_craftsman = models.BooleanField(default=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    work_from = models.TimeField(null=True)
    work_to = models.TimeField(null=True)
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_to = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    wu_choices = (
        ('AlGhoota', 'AlGhoota'),
        ('AlHamra', 'AlHamra'),
        ('AlWa3r', 'AlWa3r'),
        ('Alinshaat', 'Alinshaat'),
        ('Alhadara','Alhadara'),
    )
    work_address = models.CharField(max_length=50, choices=wu_choices, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLES, null=True, blank=True)
    #users_favourite = models.ManyToManyField(User, related_name="user_favourite", blank=True)
    def __str__(self):
        return f'{ self.user.username } Profile'
    
    class Meta:
        verbose_name = 'profile'

    @staticmethod
    def get_all_providers(): 
        return Profile.objects.all()
    @staticmethod
    def get_all_providers_by_service(service): 
        if service: 
            return Profile.objects.filter(is_craftsman=True).filter(service=service) 
        else: 
            return Profile.get_all_providers() 


class Fav(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favs')
    fav_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='fav_profile')
     
    class Meta:
        verbose_name = 'Favourite'

    def __str__(self):
        return f"Favourite by {self.profile.user.username} to {self.fav_profile.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

