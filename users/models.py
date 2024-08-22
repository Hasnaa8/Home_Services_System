from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from services.models import Service
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone

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


def validate_self_review(value):
    if value == value.instance.reviewer:
        raise ValidationError("You cannot review yourself.")
    
class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='revs')
    rev_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rev_profile', null=True)
    
    profile_username = models.CharField(max_length=50, null=True)
    profile_fname = models.CharField(max_length=50, null=True)
    profile_lname = models.CharField(max_length=50, null=True)
    
    rev_profile_username = models.CharField(max_length=50, null=True)
    rev_profile_fname = models.CharField(max_length=50, null=True)
    rev_profile_lname = models.CharField(max_length=50, null=True)
    
    rating = models.IntegerField(choices=[(1,'1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')])
    comment = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    likings = models.IntegerField(default=0)
    hatings = models.IntegerField(default=0)
    liking_users = models.ManyToManyField("Profile", related_name='liking_profiles')
    hating_users = models.ManyToManyField("Profile", related_name='hating_profiles')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Review, self).save(*args, **kwargs)

    class Meta:
        # unique_together = ('profile', 'rev_profile')
        verbose_name = 'Review'

    def __str__(self):
        return f"{self.profile.user.username} reviewed {self.rev_profile.user.username}"
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

