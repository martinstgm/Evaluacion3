from django import forms
from appWeb.choices import sexos, tipoCuenta, tipoTrabajador
from appWeb.models import Ciudad, Entrevistado, Empresa, Producto, Produccion, CustomUser
from django.core.exceptions import ValidationError
import hashlib
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.forms import formset_factory

def validar_rut(rut):
    rut_limpio = re.sub('[.-]', '', rut)  # Eliminar puntos y guiones
    if not rut_limpio[:-1].isdigit():
        return False

    rut_numeros = list(map(int, rut_limpio[:-1]))
    verificador = int(rut_limpio[-1])

    rut_numeros.reverse()
    multiplicadores = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5]
    suma = sum(x * y for x, y in zip(rut_numeros, multiplicadores))
    resto = suma % 11

    digito_verificador = 11 - resto if resto != 0 else 0

    return digito_verificador == verificador

class CustomUserCreationForm(UserCreationForm):
    rutUsuario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'11111111-1'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de usuario'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contrasena'}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar contrasena'}))
    tipoUsuario = forms.CharField(widget=forms.Select(choices=tipoCuenta,attrs={'class':'form-select'}))
    
    class Meta:
        model = CustomUser
        fields = ['rutUsuario','username','first_name','last_name','password1','password2','tipoUsuario']

    def clean_rutUsuario(self):
        rutUsuario = self.cleaned_data.get('rutUsuario')
        if not validar_rut(rutUsuario):
            raise forms.ValidationError("El rut no es valido")
        return rutUsuario
    

#no lo usamos ya que django tiene su propia verificacion, genial 
def validar_contrasena(value):
    # Validador de contraseña: al menos una mayúscula y un símbolo
    if not any(char.isupper() for char in value):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not any(char in '!@#$%^&*()-_+=<>,.?/:;|[]{}`~' for char in value):
        raise ValidationError("La contraseña debe contener al menos un símbolo.")

def validar_confirm_contra(value, password):
    # Validador de contraseña de confirmación: debe coincidir con la contraseña original
    if value != password:
        raise ValidationError("Las contraseñas no coinciden.")

class EntrevistadoForm(forms.ModelForm):
    rutEntrevistado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'22222222-2'}))
    pNombreEntrevistado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}))
    sNombreEntrevistado = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo nombre'}))
    pApellidoEntrevistado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}))
    sApellidoEntrevistado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo Apellido'}))
    fechaNacimiento = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'dd/mm/aaaa','type':'date'}))
    tipoTrabajo = forms.CharField(widget=forms.Select(choices=tipoTrabajador,attrs={'class':'form-control','placeholder':'Independiente/Dependiente'})) 
    sexo = forms.CharField(widget=forms.Select(choices=sexos,attrs={'class':'form-control'}))
    contacto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ej 56911223344'}))
    direccionEntrevistado = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Calle #1115'}))

    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'})
    )

    class Meta:
        model = Entrevistado
        fields = ['rutEntrevistado','pNombreEntrevistado','sNombreEntrevistado','pApellidoEntrevistado','sApellidoEntrevistado','fechaNacimiento','tipoTrabajo','sexo','contacto','direccionEntrevistado','ciudad']

class EmpresaForm(forms.ModelForm):
    rutEmpresa = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':''}))
    nombreEmpresa = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':''}))
    representanteLegal = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':''}))
    rutRepresentante = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':''}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':''}))

    def clean_rutEmpresa(self):
        rutEmpresa = self.cleaned_data.get('rutEmpresa')
        if not validar_rut(rutEmpresa):
            raise forms.ValidationError("El rut no es valido")
        return rutEmpresa
    
    def clean_rutRepresentante(self):
        rutRepresentante = self.cleaned_data.get('rutRepresentante')
        if not validar_rut(rutRepresentante):
            raise forms.ValidationError("Rut invalido")
        return rutRepresentante
    
    class Meta:
        model = Empresa
        fields = ['rutEmpresa','nombreEmpresa','representanteLegal','rutRepresentante','direccion']

'''class ProduccionForm(forms.ModelForm):

    class Meta:
        model = Produccion
        fields = ['cantidadProducto','producto']

ProduccionFormSet = formset_factory(ProduccionForm, extra=1)
'''
class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username','password1']

        from django import forms

class ProduccionForm(forms.ModelForm):
    agregar_mas = forms.BooleanField(initial=True, required=False, widget=forms.HiddenInput())
    cantidadProducto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placheholder':''}))
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(),empty_label='Selecciona un producto', widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Produccion
        fields = ['producto', 'cantidadProducto']

class EliminarUsuarioForm(forms.Form):
    confirmacion = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
