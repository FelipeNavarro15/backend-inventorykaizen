from django.contrib import admin
from .models import Producto, Compra, CompraPadre, Venta

# Admin para CompraPadre con compras anidadas
class CompraInline(admin.TabularInline):
    model = Compra
    extra = 1
    fields = ['producto', 'cantidad', 'costo_unitario', 'valor_venta', 'proveedor', 'notas']

class CompraPadreAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'proveedor', 'cantidad_productos', 'costo_total', 'fecha_registro']
    list_filter = ['fecha', 'proveedor']
    search_fields = ['proveedor', 'notas']
    inlines = [CompraInline]
    readonly_fields = ['costo_total', 'cantidad_productos', 'fecha_registro']

admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(CompraPadre, CompraPadreAdmin)
admin.site.register(Venta)
