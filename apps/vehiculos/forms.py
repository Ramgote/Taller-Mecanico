from django import forms
from .models import Marca, ModeloVehiculo, Vehiculo
from apps.core.forms import BootstrapFormMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class MarcaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre"]


class ModeloVehiculoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ModeloVehiculo
        fields = ["marca", "nombre"]

class VehiculoForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ["activo", "fecha_creacion"]
        widgets = {
            'placa': forms.TextInput(attrs={
                'style': 'text-transform: uppercase;', # Visualmente en mayúsculas
                'placeholder': '1237-ABC',
                'oninput': 'this.value = this.value.toUpperCase()' # Convierte mientras escribe
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 2, 
                'placeholder': 'Ingrese aqui si hay observaciones...',
                'style': 'resize: none;' # Opcional: evita que el usuario estire el cuadro manualmente
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [('', 'Seleccione tipo')] + list(self.fields['tipo_vehiculo'].choices)[1:]
        self.fields['tipo_vehiculo'].choices = choices

        self.fields['cliente'].empty_label = "Seleccione cliente"
        self.fields['marca'].empty_label = "Seleccione Marca"
        self.fields['modelo'].empty_label = "Seleccione Modelo"

        self.fields['modelo'].queryset = ModeloVehiculo.objects.none()

        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = ModeloVehiculo.objects.filter(marca_id=marca_id)
            except (ValueError, TypeError):
                pass

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')

        if not placa:
            raise ValidationError("La placa es obligatoria")

        import re

        placa = placa.upper()
        placa = re.sub(r'[^A-Z0-9]', '', placa)  

        patron = r'^\d{4}[A-Z]{3}$'

        if not re.match(patron, placa):
            raise ValidationError(
                "Formato de placa inválido, tiene que tener 4 dígitos numéricos y 3 letras. Ejemplo válido: 1234ABC"
            )
        
        from .models import Vehiculo

        from .models import Vehiculo

        qs = Vehiculo.objects.filter(placa=placa)

        # Si estamos editando, excluir el mismo registro
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Ya existe un vehículo con esta placa")

        return placa
    