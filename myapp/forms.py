from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['id', 'created_at']

    def clean(self):
        cleaned_data = super().clean()
        # TODO: add cross-field validation here
        # Example: if cleaned_data.get('is_active') and not cleaned_data.get('name'):
        #     raise forms.ValidationError("Active items must have a name.")
        return cleaned_data
