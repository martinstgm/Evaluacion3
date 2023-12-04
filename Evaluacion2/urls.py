from django.contrib import admin
from django.urls import path, include
from appWeb import views as vista
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vista.Inicio, name='menu'),
    path('dashboard/',vista.Dashboard,name='dashboard'),
    path('crearCuenta/',vista.crear_user,name='userAdd'),
    path('personalesForm/',vista.entrevistado_form,name='personalesForm'),
    path('graficoProduccionProvincia/',vista.grafico,name='graficoProdProv'),
    path('graficoVSInformal/',vista.graficoVsInformal,name='graficoVSInformal'),
    path('graficoVSSexo/',vista.graficoVsSexo,name='graficoVSSexo'),
    path('login',vista.login,name='login'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('empresaForm/<int:entrevistado_id>',vista.empresa_form,name='empresaForm'),
    path('produccion/<int:entrevistado_id>/',vista.produccion_form,name='produccion'),
    path('usuarios/',vista.lista_usuarios,name='usuarios'),
    path('entrevistados/',vista.lista_entrevistados,name='entrevistados'),
    path('eliminar_usuario/<int:user_id>/', vista.eliminar_usuario, name='eliminar_usuario'),
]
