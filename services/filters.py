import django_filters
from users.models import *  

class ProviderFilter(django_filters.FilterSet):
    fname = django_filters.CharFilter(field_name='fname', lookup_expr='icontains')
    lname = django_filters.CharFilter(field_name='lname', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['fname', 'lname']