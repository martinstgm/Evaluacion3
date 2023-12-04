from django.db import models
from appWeb.choices import sexos, tipoCuenta, tipoTrabajador
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
#Principalmente se modifica la tabla user y tipo de usuario que se habia diagramado previamente a solo el customUser ya que django tiene su propia clase de usuarios, aqui simplemente le agregamos campos segun lo requerido
class CustomUser(AbstractUser):
    userID = models.AutoField(primary_key=True,auto_created=True)
    rutUsuario = models.CharField(max_length=10)
    tipoUsuario = models.CharField(max_length=20,choices=tipoCuenta)

    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    
#En lugar de tener regiones se usaron provincias solo de la 4ta region para una especificidad mayor ya que el objetivo por el momento es solo la 4ta region y en caso de querer graficar los resultados tenia mayor sentido hacerlo por provincia que por region al ser todos de la misma region

class Provincia(models.Model):
    idProvincia = models.AutoField(primary_key=True)
    nombreProvincia = models.CharField(max_length=255)

    def __str__(self):
        return self.nombreProvincia
    
    class Meta:
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

class Ciudad(models.Model):
    idCiudad = models.AutoField(primary_key=True)
    nombreCiudad = models.CharField(max_length=255)
    provinciaCiudad = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreCiudad
    
    class Meta:
        db_table = 'ciudad'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

class Entrevistado(models.Model):
    entrevistadoID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pNombreEntrevistado = models.CharField(max_length=255)
    sNombreEntrevistado = models.CharField(max_length=255, blank=True, null=True)
    pApellidoEntrevistado = models.CharField(max_length=255)
    sApellidoEntrevistado = models.CharField(max_length=255)
    rutEntrevistado = models.CharField(max_length=15)
    fechaNacimiento = models.DateField(blank=True,null=True,verbose_name='Fecha de Nacimiento')
    ciudad = models.ForeignKey(Ciudad,on_delete=models.CASCADE)
    tipoTrabajo = models.CharField(max_length=1, choices=tipoTrabajador,default='i')
    sexo = models.CharField(max_length=1, choices=sexos, default='o')
    contacto = models.CharField(max_length=15, blank=True)
    direccionEntrevistado = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return "{} {} {} {}".format(self.pNombreEntrevistado, self.sNombreEntrevistado, self.pApellidoEntrevistado, self.sApellidoEntrevistado)

    class Meta:
        db_table = 'entrevistado'
        verbose_name = 'Entrevistado'
        verbose_name_plural = 'Entrevistados'

class Empresa(models.Model):
    empresaID = models.AutoField(primary_key=True)
    entrevistado = models.ForeignKey(Entrevistado, on_delete=models.CASCADE)
    rutEmpresa = models.CharField(max_length=15)
    nombreEmpresa = models.CharField(max_length=255)
    representanteLegal = models.CharField(max_length=255)
    rutRepresentante = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombreEmpresa

    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

class Producto(models.Model):
    productoID = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=255)

    def __str__(self):
        return self.nombreProducto

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Produccion(models.Model):
    entrevistado = models.ForeignKey(Entrevistado, on_delete=models.CASCADE, null=False, blank=False)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidadProducto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'produccion'
        verbose_name = 'Produccion'
        verbose_name_plural = 'Producciones'
