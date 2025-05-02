# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Attributes:
        is_company (BooleanField): Flag indicating if user is a service provider
        date_of_birth (DateField): User's date of birth
        field_of_work (CharField): Service category specialization
        groups (ManyToManyField): Custom related name for user groups
        user_permissions (ManyToManyField): Custom related name for user permissions
        
    Notes:
        - field_of_work choices include various service categories
        - 'All in One' providers can offer any service category
        - Custom related_names avoid clashes with auth.User
    """
    
    is_company = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    field_of_work = models.CharField(
        max_length=50,
        choices=[
            ('Air Conditioner', 'Air Conditioner'),
            ('All in One', 'All in One'),
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
        ],
        null=True,
        blank=True
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def is_valid_service_field(self, field):
        """
        Check if user can provide service in specified field.
        
        Args:
            field (str): Service category to validate
            
        Returns:
            bool: True if user can provide service in field,
                 False otherwise
        """
        return self.field_of_work == 'All in One' or self.field_of_work == field