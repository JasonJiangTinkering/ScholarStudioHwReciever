from django import forms
from .models import GameChallenger
from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 5242880
    # 100MB 104857600
    # 250MB - 214958080
    # 500MB - 429916160
    limit = 2621440
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

class hw1(forms.Form):
    email = forms.EmailField(label='Your email', max_length=200)
    file = forms.FileField(label='Pic of hw', validators=[file_size])

class glitchHw(forms.Form):
    email = forms.EmailField(label='Your email', max_length=200)
    url = forms.URLField(label='Your glitch LIVE SITE link')

class InitChallengerForm(forms.ModelForm):
    class Meta:
        model = GameChallenger
        fields = ['name', 'code', 'lockernumber', 'dietary_restrictions']

# two inputs for name, lockernubmer, and code
