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

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, label=False, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control', 'autofocus': True}))
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Letter box', 'class': 'form-control'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    confirmation = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    fraction = forms.ChoiceField(
        label = 'Choose your fraction',
        choices=[
            ('', '— No fraction —'),
            ('College of Winterhold', 'College of Winterhold'),
            ('Dark Brotherhood', 'Dark Brotherhood'),
            ('Thieves Guild', 'Thieves Guild'),
            ('Companions', 'Companions'),
            ('Imperial Legion', 'Imperial Legion'),
            ('Stormcloaks', 'Stormcloaks'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    avatar = forms.ImageField(label = 'Show us yourself', required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation = cleaned_data.get("confirmation")

        if password != confirmation:
            raise forms.ValidationError("Passwords do not match.")