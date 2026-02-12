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
        widget=forms.PasswordInput
    )

    rol = forms.ChoiceField(choices=Perfil.ROLES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            # Perfil creado por signals
            perfil = user.perfil
            perfil.rol = self.cleaned_data['rol']
            perfil.save()

        return user
