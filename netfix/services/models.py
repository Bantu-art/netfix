from django.db import models
from django.utils import timezone
from users.models import User

class Service(models.Model):
    # Define FIELD_CHOICES at class level
    FIELD_CHOICES = [
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('Housekeeping', 'Housekeeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    field = models.CharField(
        max_length=50,
        choices=FIELD_CHOICES  # Reference the class-level choices
    )
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    address = models.TextField()
    hours_needed = models.PositiveIntegerField()
    requested_at = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.service.price_per_hour * self.hours_needed
        super().save(*args, **kwargs)