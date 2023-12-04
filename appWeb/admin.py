from django.contrib import admin

from appWeb.models import Entrevistado, Empresa, Producto, Produccion, Ciudad, Provincia, CustomUser



class EntrevistadoAdmin(admin.ModelAdmin):
    list_display = ['entrevistadoID','user','pNombreEntrevistado','sNombreEntrevistado','pApellidoEntrevistado','sApellidoEntrevistado','rutEntrevistado','fechaNacimiento','ciudad','tipoTrabajo','sexo','contacto','direccionEntrevistado']

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['empresaID','entrevistado','rutEmpresa','nombreEmpresa','representanteLegal','rutRepresentante','direccion']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['productoID','nombreProducto']

class ProduccionAdmin(admin.ModelAdmin):
    list_display = ['entrevistado','producto','cantidadProducto']

class CiudadAdmin(admin.ModelAdmin):
    list_display = ['idCiudad','nombreCiudad']

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ['idProvincia','nombreProvincia']

admin.site.register(CustomUser)
admin.site.register(Entrevistado,EntrevistadoAdmin)
admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Produccion,ProduccionAdmin)
admin.site.register(Ciudad,CiudadAdmin)
admin.site.register(Provincia,ProvinciaAdmin)