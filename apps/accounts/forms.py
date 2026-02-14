from django import forms
from django.contrib.auth.models import User
from .models import Perfil

# -------- LOGIN --------

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

# -------- CREAR USUARIO --------

class CrearUsuarioForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    rol = forms.ChoiceField(
        choices=Perfil.ROLES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            perfil = user.perfil
            perfil.rol = self.cleaned_data['rol']
            perfil.save()

        return user
