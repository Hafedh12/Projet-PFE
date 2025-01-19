from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Eleve, Enseignant

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')

        labels = {
        'password1':'Password',
        'password2':'Confirm Password'
        }
    def clean_username(self):
        # Cette méthode n'est nécessaire que si vous autorisez l'utilisateur à changer son username.
        # Si le champ username est désactivé, ce code ne sera pas exécuté.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

class EleveForm(forms.ModelForm):
    date_de_naissance = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Eleve
        fields = ('profile_pic', 'date_de_naissance', 'anomalie')

class EnseignantForm(forms.ModelForm):
    class Meta():
        model = Enseignant
        fields = ('profile_pic','numero_telephone',)

