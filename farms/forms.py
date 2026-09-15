from django import forms

from .models import Farm


class FarmForm(forms.ModelForm):

    class Meta:
        model = Farm

        fields = [
            "farmer",
            "municipality",
            "barangay",
            "farm_name",
            "farm_type",
            "area",
            "latitude",
            "longitude",
        ]

        widgets = {

            "farmer": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "municipality": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "barangay": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Barangay"
                }
            ),

            "farm_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Farm name"
                }
            ),

            "farm_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Area in hectares",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a location on the map",
                    "step": "0.0000001",
                    "readonly": "readonly",
                    "id": "id_latitude"
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a location on the map",
                    "step": "0.0000001",
                    "readonly": "readonly",
                    "id": "id_longitude"
                }
            ),
        }