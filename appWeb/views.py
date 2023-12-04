from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from appWeb.models import Produccion, Entrevistado, CustomUser
from appWeb.forms import  EliminarUsuarioForm, EmpresaForm,ProduccionForm, EntrevistadoForm, LoginForm, CustomUserCreationForm
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from django.db.models import Sum, Count
from django.db import connection
from django.contrib import messages

# Create your views here.

@login_required
def Inicio(request):
    return render(request, "appWebTemplates/inicio.html")

def Dashboard(request):
    return render(request,'appWebTemplates/menuGraficos.html')

'''def VerListas(request):
    return render(request,'appWebTemplates/listasUsuarios.html')'''

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut_usuario = form.cleaned_data['rutUsuario']
            password = form.cleaned_data['password']

            user = authenticate(request, username=rut_usuario, password=password)

            if user is not None:
                login(request,user)
                return redirect('menu')
            else:
                form.add_error(None, 'Credenciales incorrectas. Intenta de nuevo')
    else:
        form = LoginForm()

    return render(request,'appWebTemplates/login.html',{'form':form})

@login_required
def grafico(request):
    #hago la query para rescatar los datos de la bd 
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT provincia.nombreProvincia, SUM(produccion.cantidadProducto) as totalProduccion
            FROM provincia as provincia
            INNER JOIN ciudad as ciudad ON provincia.idProvincia = ciudad.provinciaCiudad_id
            INNER JOIN entrevistado as entrevistado ON ciudad.idCiudad = entrevistado.ciudad_id
            INNER JOIN produccion as produccion ON entrevistado.entrevistadoID = produccion.entrevistado_id
            GROUP BY provincia.nombreProvincia
        """)
        results = cursor.fetchall()

    return render(request, 'appWebTemplates/graficoProduccionProvincia.html', {'data': results})

@login_required
def graficoVsInformal(request):
    # Consulta para contar trabajadores independientes ('i') y dependientes ('d')
    resultados = Entrevistado.objects.values('tipoTrabajo').annotate(cantidad=Count('tipoTrabajo'))

    # Prepara los datos para Highcharts
    datos = {'independientes': 0, 'dependientes': 0}

    # Llena los datos según la consulta
    for resultado in resultados:
        if resultado['tipoTrabajo'] == 'i':
            datos['independientes'] = resultado['cantidad']
        elif resultado['tipoTrabajo'] == 'd':
            datos['dependientes'] = resultado['cantidad']

    # Pasa los datos a la plantilla y renderiza
    return render(request, 'appWebTemplates/graficoVSInformal.html', {'datos': datos})

@login_required
def graficoVsSexo(request):
    valores = Entrevistado.objects.values('sexo').annotate(cantidad=Count('sexo'))
    datos = {'Otro': 0, 'Masculino': 0, 'Femenino': 0}

    for valor in valores:
        if valor['sexo'] == 'o':
            datos['Otro'] = valor['cantidad']
        elif valor['sexo'] == 'm':
            datos['Masculino'] = valor['cantidad']
        elif valor['sexo'] == 'f':
            datos['Femenino'] = valor['cantidad']

    return render(request, 'appWebTemplates/graficoVSSexo.html', {'datos': datos})


@login_required
def crear_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = CustomUserCreationForm()
    return render(request, 'appWebTemplates/crearCuentas.html',{'form':form})

'''def crear_user(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = UsuarioForm()
    return render(request, 'appWebTemplates/crearCuentas.html',{'form':form})'''

@login_required
def entrevistado_form(request):
    if request.method == 'POST':
        form = EntrevistadoForm(request.POST)
        if form.is_valid():
            entrevistado = form.save(commit=False)
            if isinstance(request.user, CustomUser):
                entrevistado.user = request.user
                entrevistado.save()
                if entrevistado.tipoTrabajo == 'i':
                    
                    return redirect('produccion',entrevistado_id = entrevistado.entrevistadoID)
                elif entrevistado.tipoTrabajo == 'd':
                    
                    return redirect('empresaForm',entrevistado_id = entrevistado.entrevistadoID)
    else:
        form = EntrevistadoForm()
    return render(request, 'appWebTemplates/entrevistadoForm.html', {'form':form})

'''@login_required
def produccion_form(request, entrevistado_id):
    ProduccionFormSet = formset_factory(ProduccionForm, extra = 1 , can_delete = True)
    if request.method == 'POST':
        formset = ProduccionFormSet(request.POST,prefix= 'produccion')
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    produccion = form.save(commit=False)

                    # Obtén la instancia de Entrevistado
                    entrevistado = Entrevistado.objects.get(pk=entrevistado_id)

                    # Asigna la instancia de Entrevistado al campo entrevistado
                    produccion.entrevistado = entrevistado

                    # Guarda la instancia de Produccion en la base de datos
                    produccion.save()

            return redirect('menu')  # Ajusta esto según tus necesidades

    else:
        formset = ProduccionFormSet(prefix='produccion')

    return render(request, 'appWebTemplates/produccion.html', {'formset': formset})'''

@login_required
def produccion_form(request, entrevistado_id):
    if request.method == 'POST':
        form = ProduccionForm(request.POST)
        if form.is_valid():
            produccion = form.save(commit=False)
            entrevistado = Entrevistado.objects.get(pk=entrevistado_id)
            produccion.entrevistado = entrevistado
            produccion.save()

            if form.cleaned_data['agregar_mas']:
                # Si se quiere agregar más productos, redirige a la misma página con un nuevo formulario
                return redirect('produccion', entrevistado_id=entrevistado_id)
            else:
                # Si no se quieren agregar más productos, redirige al menú
                return redirect('menu')  # Ajusta esto según tus necesidades
    else:
        form = ProduccionForm()

    return render(request, 'appWebTemplates/produccion.html', {'form': form})

@login_required
def empresa_form(request, entrevistado_id):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            entrevistado = Entrevistado.objects.get(pk=entrevistado_id)
            empresa = form.save(commit=False)
            empresa.entrevistado = entrevistado
            empresa.save()
            return redirect('produccion', entrevistado_id=entrevistado_id)

    else:
        form = EmpresaForm()
    return render(request, 'appWebTemplates/empresaForm.html', {'form': form})

@login_required
def lista_entrevistados(request):
    usuarioActivo = request.user
    entrevistados = Entrevistado.objects.filter(user=usuarioActivo)
    tipo_trabajo = {'i': 'Independiente', 'd': 'Dependiente'}
    for entrevistado in entrevistados:
        entrevistado.tipoTrabajo = tipo_trabajo.get(entrevistado.tipoTrabajo,'')
    data = {'entrevistados':entrevistados}
    return render(request,'appWebTemplates/entrevistados.html',data)

@login_required
def lista_usuarios(request):
    usuarios = CustomUser.objects.filter(tipoUsuario__in=['a','e'])
    tipo_usuario = {'a': 'Analista', 'e': 'Entrevistador'}
    #Asociamos los valores a o e segun correspondan con un for
    for usuario in usuarios:
        usuario.tipoUsuario = tipo_usuario.get(usuario.tipoUsuario, '')
    data = {'usuarios':usuarios}
    return render(request,'appWebTemplates/usuarios.html',data)

@login_required
def eliminar_usuario(request, user_id):
    User = get_user_model()
    usuario = get_object_or_404(User, userID=user_id)
    
    # Realizar la eliminación del usuario
    usuario.delete()
    
    return redirect('usuarios')