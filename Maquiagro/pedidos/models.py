from django.db import models
from django.contrib.auth import get_user_model
from portafolio.models import project
from django.utils import timezone

from django.db.models import F, Sum, FloatField
# Create your models here.

User=get_user_model()

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.lineapedido_set.aggregate(
            total=Sum(F("producto__price") * F("cantidad"), output_field=FloatField())
        )["total"] or FloatField(0)

    precio_total = property(total)  # Agrega un campo precio_total basado en la función total

    def __str__(self):
        # Restar 5 horas a la fecha y formatearla
        fecha_resta_cinco_horas = self.created_at - timezone.timedelta(hours=5)
        return f'Pedido {self.id} - {fecha_resta_cinco_horas.strftime("%d de %B de %Y a las %H:%M")}'
    
    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']

class LineaPedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(project, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto.title}'

    class Meta:
        db_table = 'lineapedidos'
        verbose_name = 'Linea Pedido'
        verbose_name_plural = 'Líneas Pedidos'
        ordering = ['id']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100, default='')  # Agrega un valor predeterminado
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
