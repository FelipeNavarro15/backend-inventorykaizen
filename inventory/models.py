# backend/inventory/models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q

class Producto(models.Model):
    id_producto = models.IntegerField(unique=True, null=True, blank=True, editable=False)
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    unidad_medida = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.id_producto is None:
            # Encontrar el primer número disponible
            usado = set(Producto.objects.values_list('id_producto', flat=True).distinct())
            numero = 1
            while numero in usado:
                numero += 1
            self.id_producto = numero
        super().save(*args, **kwargs)
    
    @staticmethod
    def calcular_numero_dinámico_venta(fecha_venta, venta_id=None):
        """
        Calcula el número dinámico para una venta basado en la fecha.
        Las ventas más recientes tienen números más bajos.
        Si hay múltiples ventas en la misma fecha, comparten el mismo número.
        """
        from django.db.models import F, Window
        from django.db.models.functions import Rank, DenseRank
        
        # Obtener todas las ventas
        todas_ventas = Venta.objects.all()
        
        # Obtener fechas únicas ordenadas descendente (más reciente primero)
        fechas_unicas = todas_ventas.values_list('fecha', flat=True).distinct().order_by('-fecha')
        
        # Encontrar la posición de la fecha actual
        for indice, fecha in enumerate(fechas_unicas, 1):
            if fecha == fecha_venta:
                return indice
        
        # Si no se encuentra, devolver el siguiente número
        return len(list(fechas_unicas)) + 1
    
    @staticmethod
    def calcular_numero_dinámico_compra(fecha_compra, compra_id=None):
        """
        Calcula el número dinámico para una compra basado en la fecha.
        Las compras más recientes tienen números más bajos.
        Si hay múltiples compras en la misma fecha, comparten el mismo número.
        """
        # Obtener todas las compras
        todas_compras = Compra.objects.all()
        
        # Obtener fechas únicas ordenadas descendente (más reciente primero)
        fechas_unicas = todas_compras.values_list('fecha', flat=True).distinct().order_by('-fecha')
        
        # Encontrar la posición de la fecha actual
        for indice, fecha in enumerate(fechas_unicas, 1):
            if fecha == fecha_compra:
                return indice
        
        # Si no se encuentra, devolver el siguiente número
        return len(list(fechas_unicas)) + 1
    
    @staticmethod
    def calcular_numero_dinámico_compra_padre(fecha_compra, compra_padre_id=None):
        """
        Calcula el número dinámico para una compra padre basado en la fecha.
        Las compras padre más recientes tienen números más bajos.
        Si hay múltiples compras padre en la misma fecha, comparten el mismo número.
        """
        # Obtener todas las compras padre
        todas_compras_padre = CompraPadre.objects.all()
        
        # Obtener fechas únicas ordenadas descendente (más reciente primero)
        fechas_unicas = todas_compras_padre.values_list('fecha', flat=True).distinct().order_by('-fecha')
        
        # Encontrar la posición de la fecha actual
        for indice, fecha in enumerate(fechas_unicas, 1):
            if fecha == fecha_compra:
                return indice
        
        # Si no se encuentra, devolver el siguiente número
        return len(list(fechas_unicas)) + 1
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    @property
    def stock_actual(self):
        total_compras = self.compras.aggregate(
            total=models.Sum('cantidad')
        )['total'] or 0
        
        total_ventas = self.ventas.aggregate(
            total=models.Sum('cantidad')
        )['total'] or 0
        
        return total_compras - total_ventas

# Modelo CompraPadre para agrupar múltiples compras
class CompraPadre(models.Model):
    """Agrupa múltiples productos en una sola compra"""
    numero = models.IntegerField(unique=True, null=True, blank=True, editable=False)
    fecha = models.DateField()
    proveedor = models.CharField(max_length=200)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
    
    @property
    def costo_total(self):
        return sum(compra.costo_total for compra in self.compras.all())
    
    @property
    def cantidad_productos(self):
        return self.compras.count()
    
    def __str__(self):
        return f"Compra Padre #{self.id} - {self.proveedor} ({self.fecha})"

# Modelo Compra vinculado a CompraPadre
class Compra(models.Model):
    numero = models.IntegerField(unique=True, null=True, blank=True, editable=False)
    compra_padre = models.ForeignKey(CompraPadre, on_delete=models.CASCADE, related_name='compras', null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='compras')
    fecha = models.DateField()
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    costo_unitario = models.IntegerField(validators=[MinValueValidator(1)])
    valor_venta = models.IntegerField(validators=[MinValueValidator(1)])
    proveedor = models.CharField(max_length=200)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
    
    @property
    def costo_total(self):
        return self.cantidad * self.costo_unitario
    
    def __str__(self):
        return f"Compra #{self.id} - {self.producto.nombre}"


class Venta(models.Model):
    CANALES = [
        ('local', 'Local'),
        ('whatsapp', 'WhatsApp'),
        ('telefono', 'Teléfono'),
        ('delivery', 'Delivery'),
        ('otro', 'Otro'),
    ]
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
        ('credito', 'Crédito'),
    ]
    
    numero = models.IntegerField(unique=True, null=True, blank=True, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateField()
    canal_venta = models.CharField(max_length=20, choices=CANALES, default='local')
    cliente = models.CharField(max_length=200)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.IntegerField(validators=[MinValueValidator(1)])
    pagado = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
    
    @property
    def total(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"Venta #{self.numero} - {self.producto.nombre}"