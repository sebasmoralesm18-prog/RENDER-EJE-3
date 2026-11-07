from django import forms
from .models import Usuario
from .models import Voto
from .models import Edicion, Categoria, Opcion

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'password']
        labels = {
            'nombre': 'Nombre',
            'correo': 'Correo electrónico',
            'password': 'Contraseña'
        }
        widgets = {
            'password': forms.PasswordInput()
        }

class VotoForm(forms.ModelForm):

    class Meta:
        model = Voto
        fields = ['categoria', 'opcion']


class EdicionForm(forms.ModelForm):

    class Meta:
        model = Edicion

        fields = [
            'nombre',
            'activa'
        ]

        labels = {
            'nombre': 'Nombre de la edición',
            'activa': 'Activa'
        }



class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = [
            'nombre',
            'edicion',
            'habilitada'
        ]

        labels = {
            'nombre': 'Nombre de la categoría',
            'edicion': 'Edición',
            'habilitada': 'Habilitada'
        }

        widgets = {

            'nombre': forms.TextInput(
                attrs={
                    'class': 'campo-gestion'
                }
            ),

            'edicion': forms.Select(
                attrs={
                    'class': 'campo-gestion'
                }
            ),

            'habilitada': forms.CheckboxInput(
                attrs={
                    'class': 'check-gestion'
                }
            )

        }


class EdicionForm(forms.ModelForm):

    class Meta:
        model = Edicion

        fields = [
            'nombre',
            'activa'
        ]

        labels = {
            'nombre': 'Nombre de la edición',
            'activa': 'Edición activa'
        }

        widgets = {

            'nombre': forms.TextInput(
                attrs={
                    'class': 'campo-gestion'
                }
            ),

            'activa': forms.CheckboxInput(
                attrs={
                    'class': 'check-gestion'
                }
            )

        }




class OpcionForm(forms.ModelForm):

    class Meta:
        model = Opcion

        fields = [
            'nombre',
            'categoria'
        ]

        labels = {
            'nombre': 'Nombre de la opción',
            'categoria': 'Categoría'
        }

class OpcionForm(forms.ModelForm):

    class Meta:
        model = Opcion
        fields = ['nombre', 'categoria']

        labels = {
            'nombre': 'Nombre de la opción',
            'categoria': 'Categoría'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'campo-gestion'
            }),

            'categoria': forms.Select(attrs={
                'class': 'campo-gestion'
            })
        }
