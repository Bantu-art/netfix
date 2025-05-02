from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta


class CustomerRegistrationForm(UserCreationForm):
    """
    Form for customer user registration.
    
    Attributes:
        date_of_birth (DateField): User's birth date with date picker widget
        
    Notes:
        - Extends Django's UserCreationForm
        - Includes email validation
        - Enforces minimum age of 15 years
        - Sets is_company to False on save
    """
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'date_of_birth']

    def clean_email(self):
        """
        Validate email uniqueness.
        
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email already exists
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_date_of_birth(self):
        """
        Validate user age requirement.
        
        Returns:
            date: Validated birth date
            
        Raises:
            ValidationError: If user is under 15 years old
        """
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        
        if age < 15:
            raise ValidationError("You must be at least 15 years old to register.")
        
        return date_of_birth

    def save(self, commit=True):
        """
        Save user and set is_company flag.
        
        Args:
            commit (bool): Whether to save to database
            
        Returns:
            User: Created user instance
        """
        user = super().save(commit=False)
        user.is_company = False
        if commit:
            user.save()
        return user


class CompanyRegistrationForm(UserCreationForm):
    """
    Form for service provider company registration.
    
    Attributes:
        field_of_work (ChoiceField): Service category selection
        
    Notes:
        - Extends Django's UserCreationForm
        - Includes email validation
        - Sets is_company to True on save
        - Excludes 'All in One' from field choices
    """
    
    field_of_work = forms.ChoiceField(choices=User._meta.get_field('field_of_work').choices[1:])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'field_of_work']

    def clean_email(self):
        """
        Validate email uniqueness.
        
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email already exists
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        """
        Save user and set is_company flag.
        
        Args:
            commit (bool): Whether to save to database
            
        Returns:
            User: Created user instance
        """
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
        return user