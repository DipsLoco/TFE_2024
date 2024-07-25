from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse e-mail'})
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    last_name = forms.CharField(
        label="Nom de famille",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'})
    )
    birth_date = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date de naissance', 'type': 'date'})
    )
    phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'})
    )
    address = forms.CharField(
        label="Adresse",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'})
    )
    postal_code = forms.CharField(
        label="Code postal",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code postal'})
    )
    city = forms.CharField(
        label="Ville",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'})
    )
    image = forms.ImageField(
        label="Image de profil",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'phone', 'address', 'postal_code', 'city', 'image', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nom d\'utilisateur'
        self.fields['username'].label = 'Nom d\'utilisateur'
        self.fields['username'].help_text = 'Requis. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password1'].help_text = 'Votre mot de passe doit contenir au moins 8 caractères, ne pas être couramment utilisé et ne pas être entièrement numérique.'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmez le mot de passe'
        self.fields['password2'].label = 'Confirmez le mot de passe'
        self.fields['password2'].help_text = 'Entrez le même mot de passe que précédemment, pour vérification.'
