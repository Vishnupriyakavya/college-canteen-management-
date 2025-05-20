from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'cabin_no', 'block_no', 'floor_no']
