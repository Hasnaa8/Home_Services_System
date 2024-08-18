from django.db import models

# Create your models here.
class Service(models.Model):
    services_list = [
        ('Architecture Engineering','Architecture Engineering'),
        ('carpenters','carpenters'), 
        ('decorations','decorations'),
        ('Civil Engineering','Civil Engineering'),
        ('electrician','electrician'),
        ('house painting','house painting'),
        ('movers','movers'), ('plumbers','plumbers'), 
        ('Roof insulation','Roof insulation'), 
        ('solar energy','solar energy'), 
    ]
    category = models.CharField(max_length=50,null=True,blank=True, choices=services_list)
    # image = models.ImageField(upload_to='photos/%y/%m/%d')


    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'service'

    @staticmethod
    def get_all_servicess():
        return Service.objects.all()
    