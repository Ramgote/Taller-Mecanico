from django import forms
from .models import Cliente

from apps.core.forms import BootstrapFormMixin
from django.contrib.auth.models import User
from django.contrib import messages


class ClienteForm(BootstrapFormMixin, forms.ModelForm):    
    class Meta:
        model = Cliente
        exclude = ["usuario"]
        # fields = "__all__"            
        # fields = ['nombre', 'telefono', 'nit_ci', 'usuario']
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si es RESPONSABLE → no puede cambiar usuario
        if user.perfil.rol == "RESPONSABLE":
            self.fields["usuario"].widget = forms.HiddenInput()
            self.instance.usuario = user

        # Si es SUPERADMIN → selector solo responsables
        if user.perfil.rol == "SUPERADMIN":
            from django.contrib.auth.models import User
            self.fields["usuario"].queryset = User.objects.filter(
                perfil__rol="RESPONSABLE",
                is_active=True
            )
    """ 
    