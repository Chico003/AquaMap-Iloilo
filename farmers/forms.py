from django import forms
from .models import Farmer


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [
            "municipality",
            "first_name",
            "middle_name",
            "last_name",
            "sex",
            "contact_number",
        ]

        widgets = {
            "municipality": forms.Select(
                attrs={"class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name",
                }
            ),
            "middle_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Middle name (optional)",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name",
                }
            ),
            "sex": forms.Select(
                attrs={"class": "form-control"}
            ),
            "contact_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contact number (optional)",
                }
            ),
        }