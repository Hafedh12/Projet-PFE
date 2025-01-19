from django import forms
from .models import Cours, Exercice, Solution, Status


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ('id_cours','nom_cours','fichier')


class ExerciceForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        label='Start Time',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    finish_time = forms.DateTimeField(
        label='Finish Time',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model = Exercice
        fields = ('nom_exercice','fichier','start_time','finish_time')

class Solutionform(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(Solutionform, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['exercice'].queryset = Exercice.objects.filter(créer_par=user)

    class Meta:
        model = Solution
        fields = ('exercice','fichier')


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        labels = {
            'fichier': 'Votre réponse',
        }
        fields = ('fichier',)

