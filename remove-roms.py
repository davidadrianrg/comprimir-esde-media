import sys
from pathlib import Path

# =================================================================
#                         CONFIGURACIÓN
# =================================================================

# Directorio base de las roms (donde están las carpetas emulador1, emulador2, etc.)
ROMS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\roms')

# Directorio base de las imágenes (donde están las carpetas emulador1, emulador2, etc.)
MEDIA_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\downloaded_media')

# Carpeta específica donde se buscan las imagenes (miximages)
SCREENSHOTS_FOLDER = 'miximages'

# Tipos de archivos de rom que debe buscar (se ignoran las mayúsculas/minúsculas)
# *Añade o elimina las extensiones que necesites*. 
# ¡IMPORTANTE! No incluyas el punto (.).
ROM_EXTENSIONS = [
    'zip', '7z', 'nes', 'sfc', 'n64', 'iso', 'cue', 'ccd', 'gdi', 'chd', 'm3u', 'rvz', 'dosz', 'cdi', 'dsk', 'cci', 'bin', 'pak', 'cso', 'scummvm', 'nsp', 'wua'
]

# -----------------------------------------------------------------
#                          MODO DE SEGURIDAD
# -----------------------------------------------------------------
# ⚠️ Cambia esto a 'True' SOLO cuando estés seguro de que el script
# está identificando correctamente los archivos a borrar. 
# Si es 'False', solo mostrará qué borraría.
EJECUTAR_BORRADO = False

# =================================================================
#                      FUNCIÓN DE LIMPIEZA
# =================================================================

def limpiar_roms_sin_media():
    """Busca roms que no tienen una imagen de captura de pantalla correspondiente (PNG o JPG)."""
    
    if not EJECUTAR_BORRADO:
        print("⚠️ MODO DE PRUEBA ACTIVADO. No se borrará ningún archivo. ⚠️")
        print("Para borrar archivos, cambia 'EJECUTAR_BORRADO' a True en el script.")
        print("-" * 50)
    else:
        print("🔥 MODO DE BORRADO ACTIVADO. ¡Los archivos se eliminarán! 🔥")
        print("-" * 50)

    total_roms_encontradas = 0
    total_roms_borradas = 0
    
    emulador_dirs = [d for d in ROMS_BASE_DIR.iterdir() if d.is_dir()]
    
    if not emulador_dirs:
        print(f"No se encontraron carpetas de emuladores dentro de '{ROMS_BASE_DIR}'")
        return

    # Iterar sobre cada carpeta de emulador
    for rom_dir in emulador_dirs:
        emulador_name = rom_dir.name
        
        print(f"\n## 🎮 Revisando emulador: {emulador_name}...")
        
        # 1. Definir la ruta de las capturas de pantalla
        screenshots_dir = MEDIA_BASE_DIR / emulador_name / SCREENSHOTS_FOLDER

        if not screenshots_dir.is_dir():
            print(f"   [INFO] No se encontró la carpeta de screenshots en: {screenshots_dir}")
            continue

        # 2. Buscar todas las roms en la carpeta del emulador
        rom_files = []
        for ext in ROM_EXTENSIONS:
            rom_files.extend(rom_dir.glob(f'*.{ext}'))
        
        if not rom_files:
            print(f"   [INFO] No se encontraron roms con las extensiones definidas.")
            continue
            
        total_roms_encontradas += len(rom_files)

        # 3. Iterar sobre cada rom encontrada
        for rom_path in rom_files:
            # Obtener el nombre del juego sin la extensión (ej: 'juego')
            game_name = rom_path.stem
            
            # --- INICIO DEL CAMBIO ---
            # Comprobar si existe la imagen con extensión PNG o JPG/JPEG
            
            # 3.1 Construir las rutas posibles
            screenshot_png = screenshots_dir / f'{game_name}.png'
            screenshot_jpg = screenshots_dir / f'{game_name}.jpg'
            screenshot_jpeg = screenshots_dir / f'{game_name}.jpeg' # Por si acaso

            # 3.2 Verificar la existencia
            # La rom NO TIENE imagen si ninguna de las rutas posibles existe.
            if not (screenshot_png.is_file() or screenshot_jpg.is_file() or screenshot_jpeg.is_file()):
            # --- FIN DEL CAMBIO ---

                # La imagen no existe, procedemos a (simular) borrar la rom
                if EJECUTAR_BORRADO:
                    try:
                        rom_path.unlink()  # Borra el archivo
                        print(f"   [BORRADO] 🗑️ Eliminado: {rom_path.name}")
                        total_roms_borradas += 1
                    except Exception as e:
                        print(f"   [ERROR] No se pudo borrar {rom_path.name}: {e}")
                else:
                    print(f"   [PRUEBA] 🚫 Se borraría: {rom_path.name}")
                    total_roms_borradas += 1 # Contar para el resumen

    # 4. Resumen final
    print("\n" + "=" * 50)
    print("✨ Tarea de limpieza finalizada.")
    print(f"Roms encontradas en total: {total_roms_encontradas}")
    print(f"Roms sin imagen/serían borradas: {total_roms_borradas}")
    print("=" * 50)

# =================================================================
#                      PUNTO DE ENTRADA
# =================================================================
if __name__ == "__main__":
    limpiar_roms_sin_media()

    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")