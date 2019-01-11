from django import forms
from .models import account

# create form with model
class log_form(forms.ModelForm):
    class Meta:
        model = account
        fields = ('iam','alias','passwd',)
        widgets = {
            'passwd' : forms.PasswordInput,
        }