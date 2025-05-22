import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_reactivos.settings')
django.setup()

from reactivos.models import CaducidadPorCategoria

# Lee el archivo Excel
df = pd.read_excel('tabla_categorias.xlsx')

# Renombra las columnas para que coincidan con el modelo
df = df.rename(columns={
    'Categoría': 'categoria',
    'Reactivo': 'reactivo',
    'Caducidad tras apertura': 'caducidad_tras_apertura'
})

# Recorre el DataFrame e importa cada fila
for _, row in df.iterrows():
    categoria = int(row['categoria']) if pd.notnull(row['categoria']) else None
    reactivo = str(row['reactivo']).strip() if pd.notnull(row['reactivo']) else ''
    caducidad = str(row['caducidad_tras_apertura']).strip() if pd.notnull(row['caducidad_tras_apertura']) else ''
    if categoria is not None:
        CaducidadPorCategoria.objects.update_or_create(
            categoria=categoria,
            defaults={
                'reactivo': reactivo,
                'caducidad_tras_apertura': caducidad
            }
        )

print("Importación de categorías completada.")