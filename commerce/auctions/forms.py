from django import forms
from .models import Listing, Category

class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- Select a category --"
    )

    class Meta:
        model = Listing
        fields = ['name', 'description', 'price', 'img', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter listing title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting price'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }