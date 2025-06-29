from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Remove help texts
        for field_name in self.fields:
            self.fields[field_name].help_text = ''

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
