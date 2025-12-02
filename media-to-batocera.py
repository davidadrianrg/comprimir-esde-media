import sys
import shutil
from pathlib import Path

# =================================================================
#                         CONFIGURACIÓN
# =================================================================

# Directorio base de origen (donde están los archivos consolidados de ES-DE)
MEDIA_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\downloaded_media_recortado')

# Directorio base de origen para gamelist.xml
GAMELISTS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\gamelists')

# Directorio base de destino (donde se reconstruirá la estructura para Batocera)
ROMS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\media-batocera')

# -----------------------------------------------------------------
#                          MODO DE SEGURIDAD
# -----------------------------------------------------------------
# Si es True, el script solo mostrará las acciones a realizar sin copiar nada.
# Si es False, copiará los archivos (sin sobrescribir).
MODO_PRUEBA = True

# -----------------------------------------------------------------
#          MAPEO DE SISTEMAS BATOCERA ← ES-DE
# -----------------------------------------------------------------
# Diccionario que mapea los nombres de carpetas de Batocera (key) 
# a los nombres correspondientes de ES-DE (value)
# Solo se incluyen sistemas con mapeo explícito
MAPEO_SISTEMAS = {
    # Sistemas Arcade
    'mame': 'arcade',
    'atomiswave': 'atomiswave',
    'cps': 'cps',
    'cps1': 'cps1',
    'cps2': 'cps2',
    'cps3': 'cps3',
    'daphne': 'daphne',
    'fbneo': 'fbneo',
    'model2': 'model2',
    'model3': 'model3',
    'naomi': 'naomi',
    'naomi2': 'naomi2',
    'neogeo': 'neogeo',
    'neogeocd': 'neogeocd',
    'triforce': 'triforce',
    
    # Consolas de hogar
    'nes': 'nes',
    'gamecube': 'gc',
    'megadrive': 'genesis',
    '3ds': 'n3ds',
    'n64': 'n64',
    'n64dd': 'n64dd',
    'nds': 'nds',
    'satellaview': 'satellaview',
    'snes': 'snes',
    'supracan': 'supracan',
    'switch': 'switch',
    'virtualboy': 'virtualboy',
    'wii': 'wii',
    'wiiu': 'wiiu',
    
    # Sega
    'dreamcast': 'dreamcast',
    'mastersystem': 'mastersystem',
    'segacd': 'megacd',
    'saturn': 'saturn',
    'sega32x': 'sega32x',
    'sg1000': 'sg-1000',
    'segastv': 'stv',
    
    # Sony
    'ps2': 'ps2',
    'ps3': 'ps3',
    'ps4': 'ps4',
    'psp': 'psp',
    'psvita': 'psvita',
    'psx': 'psx',
    
    # Microsoft
    'windows': 'windows',
    'xbox': 'xbox',
    'xbox360': 'xbox360',
    
    # Atari
    'atari2600': 'atari2600',
    'atari5200': 'atari5200',
    'atari7800': 'atari7800',
    'atari800': 'atari800',
    'jaguar': 'atarijaguar',
    'jaguarcd': 'atarijaguarcd',
    'lynx': 'atarilynx',
    'atarist': 'atarist',
    'atarixe': 'atarixe',
    
    # Nintendo portátiles
    'gameandwatch': 'gameandwatch',
    'gb': 'gb',
    'gba': 'gba',
    'gbc': 'gbc',
    
    # Sega portátiles
    'gamegear': 'gamegear',
    
    # Otros portátiles
    'arduboy': 'arduboy',
    'gamate': 'gamate',
    'gamecom': 'gamecom',
    'gmaster': 'gmaster',
    'gp32': 'gp32',
    'megaduck': 'megaduck',
    'ngage': 'ngage',
    'ngp': 'ngp',
    'ngpc': 'ngpc',
    'pokemini': 'pokemini',
    'supervision': 'supervision',
    'wswan': 'wswan',
    'wswanc': 'wswanc',
    
    # Computadoras
    'amiga500': 'amiga',
    'amiga1200': 'amiga1200',
    'amigacd32': 'amigacd32',
    'amstradcpc': 'amstradcpc',
    'apple2': 'apple2',
    'apple2gs': 'apple2gs',
    'archimedes': 'archimedes',
    'bbc': 'bbcmicro',
    'c128': 'c128',
    'c64': 'c64',
    'coco': 'coco',
    'dragon32': 'dragon32',
    'electron': 'electron',
    'fm7': 'fm7',
    'fmtowns': 'fmtowns',
    'msx1': 'msx',
    'msx2': 'msx2',
    'msxturbor': 'msxturbor',
    'oricatmos': 'oric',
    'pc88': 'pc88',
    'pc98': 'pc98',
    'pet': 'pet',
    'cplus4': 'plus4',
    'samcoupe': 'samcoupe',
    'ti99': 'ti99',
    'c20': 'vic20',
    'x1': 'x1',
    'x68000': 'x68000',
    'zx81': 'zx81',
    'zxspectrum': 'zxspectrum',
    
    # NEC
    'pcengine': 'pcengine',
    'pcenginecd': 'pcenginecd',
    'pcfx': 'pcfx',
    'supergrafx': 'supergrafx',
    
    # Otros sistemas
    '3do': '3do',
    'arcadia': 'arcadia',
    'astrocde': 'astrocade',
    'cdi': 'cdi',
    'amigacdtv': 'cdtv',
    'channelf': 'channel_f',
    'colecovision': 'colecovision',
    'crvision': 'crvision',
    'gx4000': 'gx4000',
    'intellivision': 'intellivision',
    'odyssey2': 'odyssey2',
    'pv1000': 'pv1000',
    'scv': 'scv',
    'vectrex': 'vectrex',
    'videopacplus': 'videopac',
    
    # Ports y miscelánea (solo mapeos explícitos)
    'adam': 'adam',
    'dos': 'dos',
    'epic': 'epic',
    'fds': 'fds',
    'flash': 'flash',
    'fpinball': 'fpinball',
    'kodi': 'kodi',
    'laserdisc': 'laserdisc',
    'lcdgames': 'lcdgames',
    'lowresnx': 'lowresnx',
    'lutro': 'lutro',
    'macintosh': 'mac',
    'multivision': 'multivision',
    'openbor': 'openbor',
    'pico8': 'pico8',
    'ports': 'ports',
    'quake': 'quake',
    'scummvm': 'scummvm',
    'solarus': 'solarus',
    'spectravideo': 'spectravideo',
    'steam': 'steam',
    'sufami': 'sufami',
    'tic80': 'tic80',
    'thomson': 'moto',
    'trs-80': 'trs-80',
    'uzebox': 'uzebox',
    'vircon32': 'vircon32',
    'vpinball': 'vpinball',
    'vsmile': 'vsmile',
    'wasm4': 'wasm4',
}

def obtener_nombre_batocera(nombre_esde: str) -> str:
    """
    Convierte el nombre del sistema de ES-DE al nombre correspondiente en Batocera.
    Busca en el diccionario invertido (key=batocera, value=es-de).
    Si no hay mapeo específico, devuelve None para omitir el sistema.
    """
    nombre_normalizado = nombre_esde.lower().strip()
    
    # Buscar el nombre de Batocera correspondiente al nombre de ES-DE
    for batocera_name, esde_name in MAPEO_SISTEMAS.items():
        if esde_name.lower().strip() == nombre_normalizado:
            return batocera_name
    
    # Si no encuentra mapeo, devuelve None para omitir
    return None

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
    if MODO_PRUEBA:
        print(f"   [PRUEBA] Se copiaria: {nombre_log}")
        # Contamos la copia que se realizaría
        return 1 
    else:
        try:
            shutil.copy2(origen, destino) # copy2 copia permisos y metadata
            print(f"   [COPIADO] Exito al copiar: {nombre_log}")
            return 1 # 1 archivo copiado
        except Exception as e:
            print(f"   [ERROR] Fallo la copia de {nombre_log}: {e}")
            return 0


def copiar_archivos_multimedia():
    """Ejecuta la lógica de copia para construir la estructura de Batocera."""
    
    if MODO_PRUEBA:
        print("MODO DE PRUEBA ACTIVADO. Solo se mostrarán las acciones.")
    else:
        print("INICIANDO COPIA DE ARCHIVOS MULTIMEDIA (No se sobrescribirán existentes).")
    print("-" * 50)
    
    total_copiados = 0
    
    # Verificar que existen los directorios de origen
    if not MEDIA_BASE_DIR.exists():
        print(f"No se encuentra el directorio de origen: '{MEDIA_BASE_DIR}'")
        return
    
    if not GAMELISTS_BASE_DIR.exists():
        print(f"No se encuentra el directorio de gamelists: '{GAMELISTS_BASE_DIR}'")
        return
    
    # Buscar carpetas de emuladores dentro de downloaded_media/
    emulador_dirs = [d for d in MEDIA_BASE_DIR.iterdir() if d.is_dir()]
    
    if not emulador_dirs:
        print(f"No se encontraron carpetas de emuladores dentro de '{MEDIA_BASE_DIR}'")
        return

    # Iterar sobre cada carpeta de emulador
    for media_dir in emulador_dirs:
        emulador_name = media_dir.name
        batocera_name = obtener_nombre_batocera(emulador_name)
        
        # Omitir sistemas sin mapeo válido
        if batocera_name is None:
            print(f"\n## [OMITIDO] Sistema sin mapeo: {emulador_name}")
            continue
        
        print(f"\n## Procesando emulador: {emulador_name} -> {batocera_name}...")
        
        # --- TAREAS DE COPIA DE MULTIMEDIA ---
        
        # 1. SCREENSHOTS -> IMAGES (screenshots/juego1.png -> batocera_name/images/juego1-image.png)
        screenshots_dir = media_dir / 'screenshots'
        if screenshots_dir.exists():
            patron_screenshots = screenshots_dir.glob('*.png')
            
            for origen_path in patron_screenshots:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'images' / f'{game_name}-image.png'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/images/{game_name}-image.png")

        # 2. COVERS -> THUMBS (covers/juego1.png -> batocera_name/images/juego1-thumb.png)
        covers_dir = media_dir / 'covers'
        if covers_dir.exists():
            patron_covers = covers_dir.glob('*.png')
            
            for origen_path in patron_covers:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'images' / f'{game_name}-thumb.png'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/images/{game_name}-thumb.png")
            
        # 3. MARQUEES (marquees/juego1.png -> batocera_name/images/juego1-marquee.png)
        marquee_dir = media_dir / 'marquees'
        if marquee_dir.exists():
            patron_marquee = marquee_dir.glob('*.png')
            
            for origen_path in patron_marquee:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'images' / f'{game_name}-marquee.png'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/images/{game_name}-marquee.png")

        # 4. VIDEOS (videos/juego1.mp4 -> batocera_name/videos/juego1-video.mp4)
        videos_dir = media_dir / 'videos'
        if videos_dir.exists():
            patron_video = videos_dir.glob('*.mp4')
            
            for origen_path in patron_video:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'videos' / f'{game_name}-video.mp4'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/videos/{game_name}-video.mp4")

        # 5. GAMELIST.XML (gamelists/emulador/gamelist.xml -> batocera_name/gamelist.xml)
        gamelist_origen = GAMELISTS_BASE_DIR / emulador_name / 'gamelist.xml'
        gamelist_destino = ROMS_BASE_DIR / batocera_name / 'gamelist.xml'
        
        if gamelist_origen.exists():
            total_copiados += copiar_fichero(gamelist_origen, gamelist_destino, f"{batocera_name}/gamelist.xml")
        else:
            print(f"   [INFO] No existe gamelist.xml para {emulador_name}")

    # Resumen final
    print("\n" + "=" * 50)
    print("Proceso de copia finalizado.")
    if MODO_PRUEBA:
         print(f"   Se realizarían {total_copiados} copias.")
         print("   Recuerda cambiar 'MODO_PRUEBA' a False para ejecutar las copias.")
    else:
        print(f"   Archivos copiados con éxito: {total_copiados}")
    print("=" * 50)

# =================================================================
#                      PUNTO DE ENTRADA
# =================================================================
if __name__ == "__main__":
    copiar_archivos_multimedia()

    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
