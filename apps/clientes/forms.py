from django import forms
from .models import Cliente

from apps.core.forms import BootstrapFormMixin


class ClienteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ["usuario"]
        # fields = "__all__"
    
