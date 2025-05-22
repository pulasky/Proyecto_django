import sys
import os
import django
import pandas as pd
from datetime import datetime

# Agrega SOLO el directorio padre del proyecto al sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_reactivos.settings')
django.setup()

from reactivos.models import CodigoReactivo, Reactivo, Pedido

# BORRAR DATOS ANTERIORES
print("Borrando datos anteriores...")
Pedido.objects.all().delete()
Reactivo.objects.all().delete()
CodigoReactivo.objects.all().delete()
print("Datos anteriores borrados.")

# Modificar la lectura del Excel
df = pd.read_excel('datos_reactivos.xlsx', engine='openpyxl')

print("\nColumnas encontradas en el Excel:")
print(df.columns.tolist())

# Limpieza básica: eliminar filas con código nulo o 0
df = df[df['Codigo'].notnull() & (df['Codigo'] != 0)]

# --- Importar CodigoReactivo (tabla base) ---
df_codigos = df.drop_duplicates(subset=['Codigo'])
for _, datos in df_codigos.iterrows():
    # Limpieza y control de errores en el código
    try:
        codigo = int(str(datos['Codigo']).strip())
    except Exception:
        print(f"❌ Código no válido: '{datos['Codigo']}' (fila ignorada)")
        continue

    # Control de categoría vacía
    categoria = None
    if pd.notnull(datos['Categoría']):
        try:
            categoria = int(datos['Categoría'])
        except Exception:
            print(f"⚠️ Categoría no válida para código {codigo}: '{datos['Categoría']}' (se guarda como None)")

    # Evita duplicados
    if not CodigoReactivo.objects.filter(codigo=codigo).exists():
        try:
            CodigoReactivo.objects.create(
                codigo=codigo,
                reactivo=str(datos['Producto']).strip() if pd.notnull(datos['Producto']) else "",
                cas=str(datos['CAS']).strip() if pd.notnull(datos['CAS']) else None,
                categoria=categoria
            )
            print(f"✔ CodigoReactivo importado: {codigo} - {datos['Producto']}")
        except Exception as e:
            print(f"❌ Error importando CodigoReactivo {codigo}: {e}")

# --- Importar Reactivos (lotes) ---
for _, datos in df.iterrows():
    try:
        codigo = int(str(datos['Codigo']).strip())
    except Exception:
        print(f"❌ Código no válido: '{datos['Codigo']}' (fila ignorada)")
        continue

    codigo_base = CodigoReactivo.objects.filter(codigo=codigo).first()
    if not codigo_base:
        print(f"❌ Reactivo con código {codigo} ignorado: Código base no encontrado.")
        continue

    fecha_entrada = pd.to_datetime(datos['Fecha entrada']).date() if pd.notnull(datos['Fecha entrada']) else None
    caducidad = pd.to_datetime(datos['Caducidad']).date() if pd.notnull(datos['Caducidad']) else None

    # Manejo seguro de capacidad
    capacidad = None
    if pd.notnull(datos['Capacidad']):
        try:
            capacidad = float(datos['Capacidad'])
        except ValueError:
            print(f"⚠️ Capacidad no numérica para Reactivo {codigo}: '{datos['Capacidad']}' (se guarda como None)")

    try:
        Reactivo.objects.create(
            codigo_base=codigo_base,
            fecha_entrada=fecha_entrada,
            lote_proveedor=datos['Lote Proveedor'] if pd.notnull(datos['Lote Proveedor']) else None,
            ud=datos['Ud.'] if pd.notnull(datos['Ud.']) else None,
            capacidad=capacidad,
            medida=datos['Medida'] if pd.notnull(datos['Medida']) else None,
            lote_eumedica=datos['LOTE Eumedica'] if pd.notnull(datos['LOTE Eumedica']) else None,
            caducidad=caducidad,
            log_book=datos['Log book'] if pd.notnull(datos['Log book']) else None,
            pag=datos['Pág.'] if pd.notnull(datos['Pág.']) else None,
            registrado_por=datos['Registrado por'] if pd.notnull(datos['Registrado por']) else None,
            stock=int(datos['Stock']) if pd.notnull(datos['Stock']) else 0,
            observaciones=datos['Observaciones'] if pd.notnull(datos['Observaciones']) else None,
        )
        print(f"✔ Reactivo importado: {codigo_base.reactivo} (Código: {codigo})")
    except Exception as e:
        print(f"❌ Error importando Reactivo {codigo}: {e}")

# --- Importar Pedidos ---
for _, datos in df.iterrows():
    try:
        codigo = int(str(datos['Codigo']).strip())
    except Exception:
        print(f"❌ Código no válido: '{datos['Codigo']}' (fila ignorada)")
        continue

    codigo_base = CodigoReactivo.objects.filter(codigo=codigo).first()
    if not codigo_base:
        print(f"❌ Pedido con código {codigo} ignorado: Código base no encontrado.")
        continue

    if pd.isnull(datos['Nº pedido']) or pd.isnull(datos['Fecha entrada']):
        print(f"❌ Pedido con código {codigo} ignorado: Nº pedido o fecha de entrada vacíos.")
        continue

    fecha_pedido = pd.to_datetime(datos['Fecha pedido']).date() if pd.notnull(datos['Fecha pedido']) else None
    precio_ud = float(str(datos['Precio Ud. (sin IVA)']).replace(',', '.')) if pd.notnull(datos['Precio Ud. (sin IVA)']) else None

    try:
        Pedido.objects.create(
            codigo_base=codigo_base,
            numero_pedido=str(datos['Nº pedido']),
            fecha_pedido=fecha_pedido,
            realizado_por=datos['Realizado por'] if pd.notnull(datos['Realizado por']) else None,
            comercial=datos['Comercial'] if pd.notnull(datos['Comercial']) else None,
            proveedor=datos['Proveedor'] if pd.notnull(datos['Proveedor']) else None,
            ref_proveedor=datos['Ref. Proveedor'] if pd.notnull(datos['Ref. Proveedor']) else None,
            precio_ud=precio_ud,
            cantidad=int(datos['Stock']) if pd.notnull(datos['Stock']) else 0,
            fecha_entrada=pd.to_datetime(datos['Fecha entrada']).date() if pd.notnull(datos['Fecha entrada']) else None,
            lote_proveedor=datos['Lote Proveedor'] if pd.notnull(datos['Lote Proveedor']) else None,
            observaciones=datos['Observaciones'] if pd.notnull(datos['Observaciones']) else None,
            recibido=True
        )
        print(f"✔ Pedido importado: {codigo_base.codigo}")
    except Exception as e:
        print(f"❌ Error con pedido {datos.get('Nº pedido')}: {e}")

