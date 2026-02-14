from django import forms

class BootstrapFormMixin:
    """
    Agrega clases Bootstrap automáticamente
    a todos los campos del formulario.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })
