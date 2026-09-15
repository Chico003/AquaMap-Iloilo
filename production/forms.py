from django import forms

from .models import ProductionRecord


class ProductionRecordForm(forms.ModelForm):

    class Meta:
        model = ProductionRecord

        fields = [
            "farm",
            "species",
            "quantity",
            "unit",
            "production_date",
            "remarks",
        ]

        widgets = {
            "farm": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "species": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Tilapia, Milkfish"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Production quantity",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "unit": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "production_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Additional remarks (optional)",
                    "rows": 4
                }
            ),
        }