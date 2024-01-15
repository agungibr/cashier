from .models import Gun
from django import forms

# - Create a record
class CreateGunForm(forms.ModelForm):

    class Meta:
        model = Gun
        fields = ['name', 'price', 'stock', 'description', 'image']


# - Update a record
class UpdateGunForm(forms.ModelForm):

    class Meta:
        model = Gun
        fields = ['name', 'price', 'stock', 'description', 'image']
