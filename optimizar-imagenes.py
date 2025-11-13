import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops
except ImportError:
    print("--- ERROR CRÍTICO ---")
    print("No se encontró la librería 'Pillow'.")
    print("Por favor, instálala abriendo una terminal (CMD o PowerShell) y escribiendo:")
    print("pip install Pillow")
    # Pausa para que el usuario pueda leer el error
    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
    sys.exit(1)


# --- CONFIGURACIÓN ---

# 1. Ruta a la carpeta 'media' principal
BASE_DIR = Path('E:\Documentos\RetroGaming\ES-DE\ES-DE\downloaded_media')

# 2. Nombre de la carpeta donde se guardarán las imágenes nuevas
OUTPUT_DIR = Path('E:\Documentos\RetroGaming\ES-DE\ES-DE\downloaded_media_recortado')

# 3. Lista de carpetas que contienen las imágenes a procesar
TARGET_FOLDERS = [
    '3dboxes', 
    'covers', 
    'marquees', 
    'miximages', 
    'screenshots', 
    'titlescreens'
]

# 4. Configuración de optimización
#    Número de colores al que se reducirá la imagen.
#    256 es el estándar para PNG-8 y ofrece una gran reducción de tamaño.
#    Puedes probar con 128 o 64 si quieres MÁS compresión (y menos calidad).
NUM_COLORES = 256

# --- FIN DE LA CONFIGURACIÓN ---


def procesar_imagenes():
    """Encuentra y procesa todas las imágenes."""
    
    # 1. Validar la carpeta de entrada
    if not BASE_DIR.is_dir():
        print(f"Error: No se encontró la carpeta de entrada: '{BASE_DIR.resolve()}'")
        print("Asegúrate de que el script esté en el lugar correcto o ajusta BASE_DIR.")
        return

    # 2. Encontrar todas las imágenes .png en las carpetas objetivo
    all_image_files = []
    print(f"Buscando imágenes .png en las siguientes carpetas: {', '.join(TARGET_FOLDERS)}")
    
    for folder_name in TARGET_FOLDERS:
        # Busca patrones como: media/emulador1/covers/*.png
        patron_busqueda = f'*/{folder_name}/*.png'
        found_files = list(BASE_DIR.glob(patron_busqueda))
        all_image_files.extend(found_files)

    if not all_image_files:
        print(f"No se encontraron imágenes .png en las carpetas especificadas dentro de '{BASE_DIR}'")
        return

    print(f"Encontradas {len(all_image_files)} imágenes. Procesando...")
    print(f"Los resultados se guardarán en: '{OUTPUT_DIR.resolve()}'")

    # 3. Procesar cada imagen
    for i, image_path in enumerate(all_image_files):
        
        # 4. Calcular la ruta de salida
        relative_path = image_path.relative_to(BASE_DIR)
        output_path = OUTPUT_DIR / relative_path

        # 5. Verificar si el archivo ya existe
        if output_path.is_file():
            print(f"\n[{i+1}/{len(all_image_files)}] Omitiendo: {image_path.name}")
            print(f"  -> Ya existe en: {output_path}")
            continue

        # 6. Crear el directorio de salida si no existe
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n[{i+1}/{len(all_image_files)}] Procesando: {image_path.name}")
        print(f"  -> Guardando en: {output_path}")

        # 7. Ejecutar la optimización (cuantización)
        try:
            with Image.open(image_path) as img:
                # Aseguramos que trabajamos con RGBA (para manejar la transparencia)
                # antes de cuantizar.
                img_rgba = img.convert('RGBA')

                # CUANTIZACIÓN: Reducimos la paleta de colores.
                # Esta es la operación "con pérdida" que reduce la calidad y el tamaño.
                # Usa el dither por defecto (Floyd-Steinberg) para mejores resultados visuales.
                quant_img = img_rgba.quantize(colors=NUM_COLORES)

                # Guardamos la nueva imagen (modo 'P' - Paleta) optimizada
                quant_img.save(
                    str(output_path), 
                    'PNG', 
                    optimize=True
                )
            
            print(f"  [ÉXITO] Imagen optimizada.")
        
        except Exception as e:
            # Si Pillow falla (ej. archivo corrupto)
            print(f"  [ERROR] Falló el procesamiento de {image_path.name}:")
            print(f"    {e}")
        
    print("\n¡Proceso completado!")

# --- Punto de entrada principal ---
if __name__ == "__main__":
    # La comprobación de Pillow se hace al inicio con el 'try...except ImportError'
    procesar_imagenes()
    
    # Pausa al final en Windows si se hace doble clic
    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
