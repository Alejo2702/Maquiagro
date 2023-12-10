from django.contrib import admin
from django.utils import timezone, numberformat
from .models import Pedido, LineaPedido
import locale

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at_formatted','precio_total_colombiano' )
    readonly_fields = ('precio_total_colombiano',)
    inlines = [LineaPedidoInline]
    
    def precio_total_colombiano(self, obj):
        # Asegurarse de que obj.precio_total es un número flotante válido
        try:
            precio_total = float(obj.precio_total)
        except (TypeError, ValueError):
            # Manejar el caso en que obj.precio_total no es un número flotante válido
            return "No válido"

        # Configurar la localidad colombiana para formatear los números
        locale.setlocale(locale.LC_ALL, 'es_CO.utf8')

        # Formatear el precio_total como moneda colombiana con puntos como separadores de miles y tres decimales
        formatted_price = locale.currency(precio_total, grouping=True, symbol='', international=True)
        return formatted_price

    precio_total_colombiano.short_description = 'Precio Total (COP)'

    def created_at_formatted(self, obj):
        # Restar un día a la fecha y formatearla
        fecha_resta_uno = obj.created_at - timezone.timedelta(hours=5)
        return fecha_resta_uno.strftime("%d-%m-%Y %H:%M:%S")
    created_at_formatted.short_description = 'Fecha del Pedido'

admin.site.register(Pedido, PedidoAdmin)