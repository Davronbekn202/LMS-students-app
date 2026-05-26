from django import forms
from .models import CustomUser
# from ..education.edu_models import Student


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password',

        ]
    def save(self, commit = True):
        data=self.cleaned_data
        username=data['username']
        email=data['email']
        password=data['password']
        user=CustomUser.objects.create_user(username=username,email=email,password=password)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
