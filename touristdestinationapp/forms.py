from django import forms
from .models import *

class TouristDestinationForm(forms.ModelForm):
    class Meta:
        model=TouristDestination
        fields='__all__'