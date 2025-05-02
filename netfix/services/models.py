from django.db import models
from django.utils import timezone
from users.models import User


class Service(models.Model):
    """
    Model representing a service offered by a company.
    
    Attributes:
        FIELD_CHOICES (list): Predefined choices for service categories
        name (CharField): Name of the service
        description (TextField): Detailed description of the service
        field (CharField): Category of the service
        price_per_hour (DecimalField): Hourly rate for the service
        created_at (DateTimeField): Timestamp when service was created
        company (ForeignKey): Reference to the service provider
    """

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
        choices=FIELD_CHOICES
    )
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')


class ServiceRequest(models.Model):
    """
    Model representing a service request from a customer.
    
    Attributes:
        service (ForeignKey): Reference to the requested service
        customer (ForeignKey): Reference to the requesting customer
        address (TextField): Location where service should be provided
        hours_needed (PositiveIntegerField): Number of hours requested
        requested_at (DateTimeField): Timestamp of the request
        total_cost (DecimalField): Total cost calculated from hours and rate
    """

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    address = models.TextField()
    hours_needed = models.PositiveIntegerField()
    requested_at = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        Override save method to calculate total cost before saving.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Notes:
            Calculates total_cost as price_per_hour * hours_needed if not already set
        """
        if not self.total_cost:
            self.total_cost = self.service.price_per_hour * self.hours_needed
        super().save(*args, **kwargs)