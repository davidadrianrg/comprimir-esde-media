import sys
import shutil
from pathlib import Path

# =================================================================
#                         CONFIGURACIÓN
# =================================================================

# Directorio base de origen (donde están las roms y los archivos fuente)
ROMS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\roms')

# Directorio base de destino (donde se consolidarán los archivos)
MEDIA_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\downloaded_media')

# -----------------------------------------------------------------
#                          MODO DE SEGURIDAD
# -----------------------------------------------------------------
# Si es True, el script solo mostrará las acciones a realizar sin copiar nada.
# Si es False, copiará los archivos (sin sobrescribir).
MODO_PRUEBA = False

# =================================================================
#                      FUNCIÓN DE COPIA
# =================================================================

def copiar_fichero(origen: Path, destino: Path, nombre_log: str):
    """
    Copia un archivo de origen a destino si no existe. 
    Maneja el modo de prueba y contabiliza la acción.
    """
    
    # 1. Crear el directorio de destino si no existe
    if not MODO_PRUEBA:
        destino.parent.mkdir(parents=True, exist_ok=True)

    # 2. Verificar si el archivo ya existe
    if destino.is_file():
        print(f"   [INFO] Ya existe: {nombre_log} - Omitiendo copia.")
        return 0 # 0 archivos copiados

    # 3. Realizar o simular la copia
    
    # --- INICIO DEL CAMBIO ---
    if MODO_PRUEBA:
        print(f"   [PRUEBA] ✅ Se copiaría: {nombre_log}")
        # Contamos la copia que se realizaría
        return 1 
    # --- FIN DEL CAMBIO ---
    
    else:
        try:
            shutil.copy2(origen, destino) # copy2 copia permisos y metadata
            print(f"   [COPIADO] ✨ Éxito al copiar: {nombre_log}")
            return 1 # 1 archivo copiado
        except Exception as e:
            print(f"   [ERROR] ❌ Falló la copia de {nombre_log}: {e}")
            return 0


def consolidar_archivos_multimedia():
    """Ejecuta la lógica de copia para los tres tipos de rutas."""
    
    if MODO_PRUEBA:
        print("⚠️ MODO DE PRUEBA ACTIVADO. Solo se mostrarán las acciones. ⚠️")
    else:
        print("🚀 INICIANDO COPIA DE ARCHIVOS (No se sobrescribirán existentes). 🚀")
    print("-" * 50)
    
    total_copiados = 0
    
    # Buscar carpetas de emuladores dentro de Roms/
    emulador_dirs = [d for d in ROMS_BASE_DIR.iterdir() if d.is_dir()]
    
    if not emulador_dirs:
        print(f"No se encontraron carpetas de emuladores dentro de '{ROMS_BASE_DIR}'")
        return

    # Iterar sobre cada carpeta de emulador (ej: 'emulador1')
    for rom_dir in emulador_dirs:
        emulador_name = rom_dir.name
        
        print(f"\n## 🎮 Procesando emulador: {emulador_name}...")
        
        # --- TAREAS DE COPIA ---
        
        # 1. MARQUEES (roms/emulador1/images/juego1-marquee.png -> media/emulador1/marquees/juego1.png)
        patron_marquee = rom_dir.glob('images/*-marquee.png')
        
        for origen_path in patron_marquee:
            game_name = origen_path.stem.replace('-marquee', '') 
            destino_path = MEDIA_BASE_DIR / emulador_name / 'marquees' / f'{game_name}.png'
            total_copiados += copiar_fichero(origen_path, destino_path, f"{emulador_name}/marquees/{game_name}.png")


        # 2. MIXIMAGES (roms/emulador1/media/images/juego1.png -> media/emulador1/miximages/juego1.png)
        patron_mix = rom_dir.glob('media/images/*.png')
        
        for origen_path in patron_mix:
            game_name = origen_path.stem
            destino_path = MEDIA_BASE_DIR / emulador_name / 'miximages' / f'{game_name}.png'
            total_copiados += copiar_fichero(origen_path, destino_path, f"{emulador_name}/miximages/{game_name}.png")

            
        # 3. VIDEOS (roms/emulador1/media/video/juego1.mp4 -> media/emulador1/videos/juego1.mp4)
        patron_video = rom_dir.glob('media/video/*.mp4')
        
        for origen_path in patron_video:
            game_name = origen_path.stem
            destino_path = MEDIA_BASE_DIR / emulador_name / 'videos' / f'{game_name}.mp4'
            total_copiados += copiar_fichero(origen_path, destino_path, f"{emulador_name}/videos/{game_name}.mp4")


    # 4. Resumen final
    print("\n" + "=" * 50)
    print("✅ Proceso de consolidación finalizado.")
    if MODO_PRUEBA:
         # Ahora el contador refleja correctamente las copias que se harían.
         print(f"   Se realizarían {total_copiados} copias.")
         print("   Recuerda cambiar 'MODO_PRUEBA' a False para ejecutar las copias.")
    else:
        print(f"   Archivos copiados con éxito: {total_copiados}")
    print("=" * 50)

# =================================================================
#                      PUNTO DE ENTRADA
# =================================================================
if __name__ == "__main__":
    consolidar_archivos_multimedia()

    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")