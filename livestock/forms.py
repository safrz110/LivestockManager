from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import CustomUser, Animal, Species, Breed

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'phone_number',
            'address', 'animal_expertise', 'profile_pic'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required except profile_pic
        required_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
        for field in required_fields:
            self.fields[field].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

class AnimalForm(forms.ModelForm):
    species = forms.ModelChoiceField(
        queryset=Species.objects.all().order_by('name'),
        empty_label="Select Species",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'species-select'})
    )
    
    breed = forms.ModelChoiceField(
        queryset=Breed.objects.none(),
        empty_label="Select Breed",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'breed-select'})
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Set required fields
        self.fields['tag_number'].required = True
        self.fields['species'].required = True
        
        # Initialize breed choices if instance has a species
        if self.instance and hasattr(self.instance, 'species') and self.instance.species:
            self.fields['breed'].queryset = Breed.objects.filter(species=self.instance.species).order_by('name')

    class Meta:
        model = Animal
        exclude = ['owner']
        widgets = {
            'tag_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tag number'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
