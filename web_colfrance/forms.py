from django import forms


class FormContacto(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    asunto = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)
