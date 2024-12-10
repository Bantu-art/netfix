from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class CustomerRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'date_of_birth']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        # Calculate age (must be at least 15 years old)
        today = date.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        
        if age < 15:
            raise ValidationError("You must be at least 15 years old to register.")
        
        return date_of_birth

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = False
        if commit:
            user.save()
        return user

class CompanyRegistrationForm(UserCreationForm):
    field_of_work = forms.ChoiceField(choices=User._meta.get_field('field_of_work').choices[1:])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'field_of_work']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
        return user