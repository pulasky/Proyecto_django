from django.db import models
from datetime import date, timedelta

class CaducidadPorCategoria(models.Model):
    categoria = models.PositiveIntegerField(unique=True)
    reactivo = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo
    caducidad_tras_apertura = models.CharField(max_length=100, help_text="Caducidad tras apertura")  # Ahora string

    def __str__(self):
        return f"{self.categoria} - {self.reactivo} - {self.caducidad_tras_apertura}"

class CodigoReactivo(models.Model):
    codigo = models.IntegerField(unique=True)
    reactivo = models.CharField(max_length=255)
    cas = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.IntegerField(blank=True, null=True)
    caducidad_tras_apertura = models.CharField(max_length=100, blank=True, null=True)  # <-- Añade esto
    def __str__(self):
        return f"{self.reactivo} ({self.codigo})"

class Reactivo(models.Model):
    codigo_base = models.ForeignKey(
        CodigoReactivo,
        on_delete=models.CASCADE,
        related_name='lotes'
    )
    fecha_entrada = models.DateField(blank=True, null=True)
    lote_proveedor = models.CharField(max_length=100, blank=True, null=True)
    ud = models.CharField(max_length=50, blank=True, null=True)
    capacidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    medida = models.CharField(max_length=50, blank=True, null=True)
    lote_eumedica = models.CharField(max_length=100, blank=True, null=True)
    caducidad = models.DateField(blank=True, null=True)
    log_book = models.CharField(max_length=100, blank=True, null=True)
    pag = models.CharField(max_length=50, blank=True, null=True)
    registrado_por = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def obtener_alerta(self):
        hoy = date.today()
        proximidad = hoy + timedelta(days=30)
        if self.caducidad and self.caducidad < hoy:
            return 'caducado'
        elif self.caducidad and self.caducidad <= proximidad:
            return 'proximo'
        elif self.stock is not None and self.stock <= 1:
            return 'stock_bajo'
        return ''

    def __str__(self):
        return f"{self.codigo_base.reactivo} ({self.codigo_base.codigo}) - Lote {self.lote_proveedor or ''}"

class Movimiento(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    codigo_base = models.ForeignKey(CodigoReactivo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateField(default=date.today)
    cantidad_envases = models.PositiveIntegerField()
    lote_proveedor = models.CharField(max_length=100, blank=True, null=True)
    lote_eumedica = models.CharField(max_length=100, blank=True, null=True)
    capacidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    medida = models.CharField(max_length=50, blank=True, null=True)
    caducidad = models.DateField(blank=True, null=True)
    log_book = models.CharField(max_length=100, blank=True, null=True)
    pag = models.CharField(max_length=50, blank=True, null=True)
    registrado_por = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    producto = models.CharField(max_length=255, blank=True, null=True)  # Nombre textual del producto
    ud = models.CharField(max_length=50, blank=True, null=True)         # Unidad
    salidas_acum = models.IntegerField(blank=True, null=True)           # Salidas acumuladas
    stock = models.IntegerField(blank=True, null=True)                  # Stock en ese movimiento

    def __str__(self):
        return f"{self.tipo.title()} - {self.codigo_base.reactivo} ({self.cantidad_envases})"

class Pedido(models.Model):
    codigo_base = models.ForeignKey(CodigoReactivo, on_delete=models.CASCADE)
    numero_pedido = models.CharField(max_length=100)
    fecha_pedido = models.DateField(blank=True, null=True)
    realizado_por = models.CharField(max_length=100, blank=True, null=True)
    comercial = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    ref_proveedor = models.CharField(max_length=100, blank=True, null=True)
    precio_ud = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    fecha_entrada = models.DateField(blank=True, null=True)
    lote_proveedor = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    recibido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_pedido} - {self.codigo_base.codigo}"
