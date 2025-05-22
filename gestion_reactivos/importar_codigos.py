import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_reactivos.settings')
django.setup()

from reactivos.models import CodigoReactivo

# Ruta a tu archivo Excel
excel_path = 'datos_codigos_reactivos.xlsx'

# Lee el Excel
df = pd.read_excel(excel_path)

# Renombra columnas para que coincidan con los campos del modelo
df = df.rename(columns={
    'CÓDIGO': 'codigo',
    'REACTIVO / DISOLUCIÓN': 'reactivo',
    'Nº CAS': 'cas',
    'Categoría': 'categoria',
    'Caducidad tras apertura': 'caducidad_tras_apertura',
})

# Limpia filas sin código
df = df[df['codigo'].notnull() & (df['codigo'] != 0)]

# Recorre el DataFrame y actualiza o crea cada código
for _, row in df.iterrows():
    codigo = int(row['codigo'])
    valor_caducidad = row['caducidad_tras_apertura']
    if pd.isnull(valor_caducidad) or str(valor_caducidad).strip().lower() == 'none':
        valor_caducidad = ''
    defaults = {
        'reactivo': str(row['reactivo']) if pd.notnull(row['reactivo']) else '',
        'cas': str(row['cas']) if pd.notnull(row['cas']) else '',
        'categoria': int(row['categoria']) if pd.notnull(row['categoria']) else None,
        'caducidad_tras_apertura': str(valor_caducidad).strip(),
    }
    CodigoReactivo.objects.update_or_create(
        codigo=codigo,
        defaults=defaults
    )

print("Importación completada. Códigos actualizados o añadidos.")