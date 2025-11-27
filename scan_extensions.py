import os
from pathlib import Path
from collections import defaultdict

# Ruta a la carpeta de ROMs
roms_path = Path(r'E:\Documentos\RetroGaming\roms')

if not roms_path.exists():
    print(f'La carpeta {roms_path} no existe')
    exit()

# Diccionario para contar extensiones
extension_counts = defaultdict(int)
all_files = []

# Escanear recursivamente todos los archivos
print('Escaneando archivos en:', roms_path)
for file_path in roms_path.rglob('*'):
    if file_path.is_file():
        ext = file_path.suffix.lower()
        if ext:
            extension_counts[ext] += 1
            all_files.append(file_path)

# Mostrar resultados
print(f'\nTotal de archivos encontrados: {len(all_files)}')
print(f'Total de extensiones únicas: {len(extension_counts)}')

print('\nExtensiones encontradas (ordenadas por frecuencia):')
for ext, count in sorted(extension_counts.items(), key=lambda x: x[1], reverse=True):
    print(f'  {ext}: {count} archivos')

print('\nLista de extensiones para el script:')
extensions_list = sorted(extension_counts.keys())
python_extensions = ',\n    '.join([f"'{ext}'" for ext in extensions_list])
print(f'ROM_EXTENSIONS = {{\n    {python_extensions}\n}}')

# Guardar en un archivo de texto
with open('extensiones_encontradas.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total de archivos: {len(all_files)}\n')
    f.write(f'Total de extensiones únicas: {len(extension_counts)}\n\n')
    f.write('Extensiones encontradas (ordenadas por frecuencia):\n')
    for ext, count in sorted(extension_counts.items(), key=lambda x: x[1], reverse=True):
        f.write(f'  {ext}: {count} archivos\n')
    
    f.write('\n\nLista para el script:\n')
    f.write(f'ROM_EXTENSIONS = {{\n    {python_extensions}\n}}\n')

print('\nResultados guardados en: extensiones_encontradas.txt')
