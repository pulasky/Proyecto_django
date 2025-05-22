from django import forms
from .models import CodigoReactivo, Reactivo, Movimiento, Pedido, CaducidadPorCategoria, Movimiento

class CodigoReactivoForm(forms.ModelForm):
    class Meta:
        model = CodigoReactivo
        fields = ['codigo', 'reactivo', 'cas', 'categoria']

class ReactivoForm(forms.ModelForm):
    class Meta:
        model = Reactivo
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        exclude = ['fecha_entrada', 'lote_proveedor']

class EditarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class SalidaReactivoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['codigo_base', 'lote_eumedica', 'cantidad_envases', 'registrado_por', 'observaciones']

class CaducidadPorCategoriaForm(forms.ModelForm):
    class Meta:
        model = CaducidadPorCategoria
        fields = ['categoria', 'caducidad_tras_apertura']

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        exclude = ['tipo']  # Tipo es fijo: 'salida'
