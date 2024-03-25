from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Service(models.Model):
    services_list = [
        ('air conditioning','air conditioning'),
        ('aliminume fitting','aliminume fitting'),
        ('Architecture Engineering','Architecture Engineering'),
        ('Blacksmith','Blacksmith'), ('carpenters','carpenters'), 
        ('Ceramics and tiling','Ceramics and tiling'),
        ('decorastions','decorastions'),
        ('Civil Engineering','Civil Engineering'),
        ('electrician','electrician'),
        ('glass','glass'), ('house painting','house painting'),
        ('movers','movers'), ('plumbers','plumbers'), 
        ('Roof insulation','Roof insulation'), 
        ('solar energy','solar energy'), 
        ('Central gas installations','Central gas installations')
    ]
    category = models.CharField(max_length=50,null=True,blank=True, choices=services_list)
    image = models.ImageField(upload_to='photos/%y/%m/%d')
    cost_domain = models.CharField(max_length=50)


    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'category'
        #ordering = ['-price']

    @staticmethod
    def get_all_servicess():
        return Service.objects.all()
    
    @staticmethod
    def get_all_services_by_categoryid(category_id):
        if category_id:
            return Service.objects.filter(category=category_id)
        else:
            return Service.get_all_services()