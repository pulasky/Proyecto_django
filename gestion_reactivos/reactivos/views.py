from django.shortcuts import render, redirect, get_object_or_404
from .forms import CodigoReactivoForm, ReactivoForm, PedidoForm, EditarPedidoForm, SalidaReactivoForm, CaducidadPorCategoriaForm, MovimientoForm
from .models import CodigoReactivo, Reactivo, CaducidadPorCategoria, Pedido, Movimiento
from datetime import date

# --- Página de inicio ---
def home(request):
    lotes = Reactivo.objects.select_related('codigo_base').order_by('-fecha_entrada')
    from datetime import date
    for lote in lotes:
        if lote.caducidad:
            lote.dias_restantes = (lote.caducidad - date.today()).days
        else:
            lote.dias_restantes = None
    return render(request, 'reactivos/home.html', {'lotes': lotes})

# --- Lista de codigos ---
def lista_codigos(request):
    codigos = CodigoReactivo.objects.all().order_by('codigo')
    return render(request, 'reactivos/lista_codigos.html', {'codigos': codigos})

# --- Añadir nuevo reactivo ---
def nuevo_reactivo(request):
    if request.method == 'POST':
        form = CodigoReactivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_codigos')
    else:
        form = CodigoReactivoForm()
    return render(request, 'reactivos/formulario_reactivo.html', {'form': form})

# --- Eliminar reactivo ---
def eliminar_reactivo(request, pk):
    reactivo = get_object_or_404(CodigoReactivo, pk=pk)
    if request.method == 'POST':
        reactivo.delete()
        return redirect('lista_codigos')
    return render(request, 'reactivos/confirmar_eliminar.html', {'reactivo': reactivo})

# --- Lista de lotes ---
def lista_lotes(request):
    lotes = Reactivo.objects.select_related('codigo_base').order_by('-fecha_entrada')
    from datetime import date
    for lote in lotes:
        if lote.caducidad:
            lote.dias_restantes = (lote.caducidad - date.today()).days
        else:
            lote.dias_restantes = None
    return render(request, 'reactivos/lista_lotes.html', {'lotes': lotes})

# --- Lista de caducidades ---
# def lista_caducidades(request):
#     caducidades = CaducidadPorCategoria.objects.all().order_by('categoria')
#     return render(request, 'reactivos/lista_caducidades.html', {'caducidades': caducidades})

# --- Editar lote ---
def editar_lote(request, pk):
    lote = get_object_or_404(Reactivo, pk=pk)
    if request.method == 'POST':
        form = ReactivoForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReactivoForm(instance=lote)
    return render(request, 'reactivos/formulario_lote.html', {'form': form, 'lote': lote})

# --- Eliminar lote ---
def eliminar_lote(request, pk):
    lote = get_object_or_404(Reactivo, pk=pk)
    if request.method == 'POST':
        lote.delete()
        return redirect('home')
    return render(request, 'reactivos/confirmar_eliminar_lote.html', {'lote': lote})

# --- Nueva salida ---
def nueva_salida(request):
    if request.method == 'POST':
        form = SalidaReactivoForm(request.POST)
        if form.is_valid():
            salida = form.save(commit=False)
            salida.tipo = 'salida'
            # Buscar el lote correspondiente
            try:
                lote = Reactivo.objects.get(
                    codigo_base=salida.codigo_base,
                    lote_eumedica=salida.lote_eumedica
                )
                # Copiar datos del lote al movimiento
                salida.lote_proveedor = lote.lote_proveedor
                salida.ud = lote.ud
                salida.capacidad = lote.capacidad
                salida.medida = lote.medida
                salida.observaciones = lote.observaciones
                salida.stock = lote.stock
                salida.save()
                # Actualizar stock
                if lote.stock is not None:
                    lote.stock -= salida.cantidad_envases
                    lote.save()
            except Reactivo.DoesNotExist:
                # Si no existe el lote, puedes manejar el error aquí
                pass
            return redirect('lista_salidas')
    else:
        form = SalidaReactivoForm()
    return render(request, 'reactivos/formulario_salida.html', {'form': form})

# --- Lista de salidas ---
def lista_salidas(request):
    salidas = Movimiento.objects.filter(tipo='salida').select_related('codigo_base').order_by('-fecha')
    return render(request, 'reactivos/lista_salidas.html', {'salidas': salidas})

# --- Lista de pedidos ---
def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('codigo_base').all().order_by('-fecha_pedido')
    return render(request, 'reactivos/lista_pedidos.html', {'pedidos': pedidos})

# --- Nuevo pedido ---
def nuevo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'reactivos/formulario_pedido.html', {'form': form})

# --- Editar pedido ---
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = EditarPedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            # Aquí puedes crear el Reactivo si se añadió fecha_entrada
            if form.cleaned_data.get('fecha_entrada'):
                from .models import Reactivo
                Reactivo.objects.get_or_create(
                    codigo_base=pedido.codigo_base,
                    fecha_entrada=pedido.fecha_entrada,
                    lote_proveedor=pedido.lote_proveedor,
                )
            return redirect('lista_pedidos')
    else:
        form = EditarPedidoForm(instance=pedido)
    return render(request, 'reactivos/formulario_pedido.html', {'form': form, 'editar': True, 'pedido': pedido})

# --- Editar reactivo ---
def editar_reactivo(request, pk):
    reactivo = get_object_or_404(CodigoReactivo, pk=pk)
    if request.method == 'POST':
        form = CodigoReactivoForm(request.POST, instance=reactivo)
        if form.is_valid():
            form.save()
            return redirect('lista_codigos')
    else:
        form = CodigoReactivoForm(instance=reactivo)
    return render(request, 'reactivos/formulario_reactivo.html', {'form': form, 'reactivo': reactivo})

# --- Nuevo lote ---
def nuevo_lote(request):
    if request.method == 'POST':
        form = ReactivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReactivoForm()
    return render(request, 'reactivos/formulario_lote.html', {'form': form})

# --- Lista de categorias ---
def lista_categorias(request):
    categorias = CaducidadPorCategoria.objects.all().order_by('categoria')
    return render(request, 'reactivos/lista_categorias.html', {'categorias': categorias})

# --- Nueva categoria ---
def nueva_categoria(request):
    if request.method == 'POST':
        form = CaducidadPorCategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CaducidadPorCategoriaForm()
    return render(request, 'reactivos/formulario_categoria.html', {'form': form})

# --- Editar salida ---
def editar_salida(request, pk):
    salida = get_object_or_404(Movimiento, pk=pk, tipo='salida')

    if request.method == 'POST':
        form = MovimientoForm(request.POST, instance=salida)
        if form.is_valid():
            form.save()
            return redirect('lista_salidas')  # Asegúrate de tener esta vista con este nombre
    else:
        form = MovimientoForm(instance=salida)

    return render(request, 'reactivos/editar_salida.html', {'form': form, 'salida': salida})

# --- Eliminar salida ---
def eliminar_salida(request, pk):
    salida = get_object_or_404(Movimiento, pk=pk, tipo='salida')

    if request.method == 'POST':
        salida.delete()
        return redirect('lista_salidas')

    return render(request, 'reactivos/confirmar_eliminar_salida.html', {'salida': salida})
