from django.db import models
from django.db.models import Sum


class MockEndpointManager(models.Manager):
    def get_most_hit_endpoints(self):
        return self.select_related('service').order_by('-hit_count')[:10]

    def get_service_endpoints(self, service_id):
        return self.select_related('service').filter(service__id=service_id)

    def get_total_endpoints_count(self):
        return self.all().count()

    def get_total_endpoints_hit_count(self):
        return self.all().aggregate(total=Sum('hit_count'))['total']


class MockServiceManager(models.Manager):
    def get_total_service_count(self):
        return self.all().count()

    def get_services_by_user(self, user):
        return self.filter(user=user).values('id', 'name')
