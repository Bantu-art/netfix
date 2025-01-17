from django import forms
from .models import Service, ServiceRequest

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'field', 'price_per_hour']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.field_of_work != 'All in One':
            self.fields['field'].initial = user.field_of_work
            self.fields['field'].widget.attrs['readonly'] = True
            self.fields['field'].choices = [(user.field_of_work, user.field_of_work)]

    def clean_field(self):
        field = self.cleaned_data.get('field')
        user = self.initial.get('user')
        if user and user.field_of_work != 'All in One' and field != user.field_of_work:
            raise forms.ValidationError("You can only create services in your field of work.")
        return field

    def clean_price_per_hour(self):
        price = self.cleaned_data.get('price_per_hour')
        if price > 1000:
            raise forms.ValidationError("Price per hour cannot exceed 1000.")
        return price

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['address', 'hours_needed']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'hours_needed': forms.NumberInput(attrs={'min': 1, 'max': 8760})
        }

    def clean_hours_needed(self):
        hours = self.cleaned_data.get('hours_needed')
        if hours < 1:
            raise forms.ValidationError("Service hours must be at least 1.")
        if hours > 8760:
            raise forms.ValidationError("Service hours cannot exceed 8760 (1 year).")
        return hours