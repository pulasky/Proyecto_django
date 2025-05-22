import os
import sys
import django
import pandas as pd
from datetime import datetime

# ✅ 1. Configurar entorno Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_reactivos.settings')
django.setup()

# ✅ 2. Importar modelos (después de configurar Django)
from reactivos.models import Movimiento, CodigoReactivo, Reactivo

# ✅ 3. Leer Excel
archivo = 'datos_salidas.xlsx'
df = pd.read_excel(archivo, engine='openpyxl')

# Limpiar nombres de columnas
df.columns = [col.strip() for col in df.columns]

# ✅ 4. Procesar filas
for index, fila in df.iterrows():
    try:
        codigo = int(fila['Código'])
        lote_eumedica = str(fila['LOTE Eumedica']).strip()

        # Buscar CodigoReactivo
        codigo_reactivo = CodigoReactivo.objects.filter(codigo=codigo).first()
        if not codigo_reactivo:
            print(f"❌ Fila {index + 2}: CódigoReactivo {codigo} no encontrado.")
            continue

        # Buscar Reactivo por codigo y lote_eumedica
        reactivo = Reactivo.objects.filter(codigo_base=codigo_reactivo, lote_eumedica=lote_eumedica).first()
        if not reactivo:
            print(f"❌ Fila {index + 2}: Reactivo no encontrado (Código {codigo}, Lote {lote_eumedica}).")
            continue

        # Convertir fecha
        fecha = None
        if pd.notnull(fila['Fecha']):
            fecha = pd.to_datetime(fila['Fecha']).date()

        # Cantidad a restar del stock
        cantidad_envases = 1
        if pd.notnull(fila['Ud.']):
            try:
                cantidad_envases = int(fila['Ud.'])
            except:
                print(f"⚠️ Fila {index + 2}: valor de 'Ud.' inválido → se usa 1")

        # Crear Movimiento
        movimiento = Movimiento.objects.create(
            tipo='salida',
            codigo_base=codigo_reactivo,
            fecha=fecha,
            producto=fila.get('Producto'),
            lote_proveedor=fila.get('Lote Proveedor'),
            lote_eumedica=lote_eumedica,
            capacidad=float(fila['Capacidad']) if pd.notnull(fila['Capacidad']) else None,
            medida=fila.get('Medida'),
            ud=fila.get('Ud.'),
            salidas_acum=int(fila['Salidas acum.']) if pd.notnull(fila['Salidas acum.']) else None,
            stock=int(fila['Stock']) if pd.notnull(fila['Stock']) else None,
            registrado_por=fila.get('Registrado por'),
            observaciones=fila.get('Observaciones'),
            cantidad_envases=cantidad_envases
        )
        print(f"✔ Se ha creado: {movimiento}")

        # Actualizar stock del Reactivo
        if reactivo.stock is None:
            reactivo.stock = 0
        reactivo.stock -= cantidad_envases
        reactivo.save()

        print(f"✔ Fila {index + 2}: Stock actualizado −{cantidad_envases} → nuevo stock: {reactivo.stock}")

    except Exception as e:
        print(f"❌ Error en fila {index + 2}: {e}")
