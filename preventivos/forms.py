from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Empresa 

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)



class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'direccion', 'telefono']
