from django import forms
from .models import Cliente

from apps.core.forms import BootstrapFormMixin
from django.contrib import messages

class ClienteForm(BootstrapFormMixin, forms.ModelForm):    
    class Meta:
        model = Cliente
        fields = ["nombre", "telefono", "telefono_alt", "nit_ci"]
