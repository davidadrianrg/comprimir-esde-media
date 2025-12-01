import sys
import shutil
from pathlib import Path

# =================================================================
#                         CONFIGURACIÓN
# =================================================================

# Directorio base de origen (donde están los archivos consolidados de ES-DE)
MEDIA_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\downloaded_media_recortado')

# Directorio base de destino (donde se reconstruirá la estructura original)
ROMS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\media-batocera')

# -----------------------------------------------------------------
#                          MODO DE SEGURIDAD
# -----------------------------------------------------------------
# Si es True, el script solo mostrará las acciones a realizar sin copiar nada.
# Si es False, copiará los archivos (sin sobrescribir).
MODO_PRUEBA = False

# -----------------------------------------------------------------
#          MAPEO DE SISTEMAS ES-DE → BATOCERA
# -----------------------------------------------------------------
# Diccionario que mapea los nombres de carpetas de ES-DE a los nombres correctos de Batocera
# Actualizado con 105 sistemas adicionales basados en análisis exhaustivo
MAPEO_SISTEMAS = {
    # Sistemas Arcade
    'arcade': 'mame',
    'atomiswave': 'atomiswave',
    'cps': 'cps',
    'cps1': 'cps1',
    'cps2': 'cps2',
    'cps3': 'cps3',
    'daphne': 'daphne',
    'fbneo': 'fbneo',
    'mame': 'mame',
    'mame-advmame': 'mame',
    'model2': 'model2',
    'model3': 'model3',
    'naomi': 'naomi',
    'naomi2': 'naomi2',
    'naomigd': 'naomi',
    'neogeo': 'neogeo',
    'neogeocd': 'neogeocd',
    'neogeocdjp': 'neogeocd',
    'triforce': 'triforce',
    
    # Consolas de hogar
    'famicom': 'nes',
    'gc': 'gamecube',
    'genesis': 'megadrive',
    'n3ds': '3ds',
    'n64': 'n64',
    'n64dd': 'n64dd',
    'nds': 'nds',
    'nes': 'nes',
    'nesh': 'nes',
    'satellaview': 'satellaview',
    'sfc': 'snes',
    'snes': 'snes',
    'snes-msu1': 'snes',
    'snesh': 'snes',
    'snesna': 'snes',
    'supracan': 'supracan',
    'switch': 'switch',
    'virtualboy': 'virtualboy',
    'wii': 'wii',
    'wiiu': 'wiiu',
    
    # Sega
    'dreamcast': 'dreamcast',
    'genh': 'megadrive',
    'mark3': 'mastersystem',
    'mastersystem': 'mastersystem',
    'megacd': 'segacd',
    'megacdjp': 'segacd',
    'megadrive': 'megadrive',
    'megadrivejp': 'megadrive',
    'msu-md': 'megadrive',
    'saturn': 'saturn',
    'saturnjp': 'saturn',
    'sega32x': 'sega32x',
    'sega32xjp': 'sega32x',
    'sega32xna': 'sega32x',
    'segacd': 'segacd',
    'sg-1000': 'sg1000',
    'sgb': 'snes',
    'stv': 'segastv',
    
    # Sony
    'ps2': 'ps2',
    'ps3': 'ps3',
    'ps4': 'ps4',
    'psp': 'psp',
    'psvita': 'psvita',
    'psx': 'psx',
    
    # Microsoft
    'windows': 'windows',
    'windows3x': 'windows',
    'windows9x': 'windows',
    'xbox': 'xbox',
    'xbox360': 'xbox360',
    
    # Atari
    'atari2600': 'atari2600',
    'atari5200': 'atari5200',
    'atari7800': 'atari7800',
    'atari800': 'atari800',
    'atarijaguar': 'jaguar',
    'atarijaguarcd': 'jaguarcd',
    'atarilynx': 'lynx',
    'atarist': 'atarist',
    'atarixe': 'atarixe',
    
    # Nintendo portátiles
    'gameandwatch': 'gameandwatch',
    'gb': 'gb',
    'gba': 'gba',
    'gbah': 'gba',
    'gbc': 'gbc',
    'gbch': 'gbc',
    'gbh': 'gb',
    
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
    'amiga': 'amiga500',
    'amiga1200': 'amiga1200',
    'amiga500': 'amiga500',
    'amiga600': 'amiga500',
    'amigacd32': 'amigacd32',
    'amstradcpc': 'amstradcpc',
    'apple2': 'apple2',
    'apple2gs': 'apple2gs',
    'archimedes': 'archimedes',
    'bbcmicro': 'bbc',
    'c128': 'c128',
    'c64': 'c64',
    'coco': 'coco',
    'dragon32': 'dragon32',
    'electron': 'electron',
    'fm7': 'fm7',
    'fmtowns': 'fmtowns',
    'msx': 'msx1',
    'msx1': 'msx1',
    'msx2': 'msx2',
    'msxturbor': 'msxturbor',
    'oric': 'oricatmos',
    'pc88': 'pc88',
    'pc98': 'pc98',
    'pet': 'pet',
    'plus4': 'cplus4',
    'samcoupe': 'samcoupe',
    'ti99': 'ti99',
    'vic20': 'c20',
    'x1': 'x1',
    'x68000': 'x68000',
    'zx81': 'zx81',
    'zxspectrum': 'zxspectrum',
    
    # NEC
    'pcengine': 'pcengine',
    'pcenginecd': 'pcenginecd',
    'pcfx': 'pcfx',
    'supergrafx': 'supergrafx',
    'tg-cd': 'pcenginecd',
    'tg16': 'pcengine',
    
    # Bandai
    'wonderswan': 'wswan',
    'wonderswancolor': 'wswanc',
    
    # Otros sistemas
    '3do': '3do',
    'arcadia': 'arcadia',
    'astrocade': 'astrocde',
    'cdi': 'cdi',
    'cdimono1': 'cdi',
    'cdtv': 'amigacdtv',
    'channel_f': 'channelf',
    'channelf': 'channelf',
    'colecovision': 'colecovision',
    'crvision': 'crvision',
    'gx4000': 'gx4000',
    'intellivision': 'intellivision',
    'odyssey2': 'odyssey2',
    'pv1000': 'pv1000',
    'scv': 'scv',
    'vectrex': 'vectrex',
    'videopac': 'videopacplus',
    
    # Ports y miscelánea
    'adam': 'adam',
    'ags': 'ports',
    'android': 'ports',
    'chailove': 'ports',
    'consolearcade': 'ports',
    'desktop': 'ports',
    'doom': 'ports',
    'dos': 'dos',
    'easyrpg': 'ports',
    'emulators': 'ports',
    'epic': 'epic',
    'fba': 'fbneo',
    'fds': 'fds',
    'flash': 'flash',
    'fpinball': 'fpinball',
    'j2me': 'ports',
    'kodi': 'kodi',
    'laserdisc': 'laserdisc',
    'lcdgames': 'lcdgames',
    'linux': 'ports',
    'lowresnx': 'lowresnx',
    'lutro': 'lutro',
    'mac': 'macintosh',
    'mess': 'mame',
    'moto': 'thomson',
    'mugen': 'ports',
    'multivision': 'multivision',
    'openbor': 'openbor',
    'palm': 'ports',
    'pc': 'ports',
    'pcarcade': 'ports',
    'pico8': 'pico8',
    'ports': 'ports',
    'quake': 'quake',
    'scummvm': 'scummvm',
    'solarus': 'solarus',
    'spectravideo': 'spectravideo',
    'steam': 'steam',
    'sufami': 'sufami',
    'symbian': 'ports',
    'tic80': 'tic80',
    'to8': 'thomson',
    'trs-80': 'trs-80',
    'type-x': 'ports',
    'uzebox': 'uzebox',
    'vircon32': 'vircon32',
    'vpinball': 'vpinball',
    'vsmile': 'vsmile',
    'wasm4': 'wasm4',
    'xbplay2': 'ports',
    'zmachine': 'ports',
}

def obtener_nombre_batocera(nombre_esde: str) -> str:
    """
    Convierte el nombre del sistema de ES-DE al nombre correspondiente en Batocera.
    Si no hay mapeo específico, usa el nombre original en minúsculas.
    """
    nombre_normalizado = nombre_esde.lower().strip()
    return MAPEO_SISTEMAS.get(nombre_normalizado, nombre_normalizado)

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


def revertir_archivos_multimedia():
    """Ejecuta la lógica de copia inversa para reconstruir la estructura original."""
    
    if MODO_PRUEBA:
        print("MODO DE PRUEBA ACTIVADO. Solo se mostrarán las acciones.")
    else:
        print("INICIANDO REVERSIÓN DE ARCHIVOS (No se sobrescribirán existentes).")
    print("-" * 50)
    
    total_copiados = 0
    
    # Verificar que existe el directorio de origen
    if not MEDIA_BASE_DIR.exists():
        print(f"No se encuentra el directorio de origen: '{MEDIA_BASE_DIR}'")
        return
    
    # Buscar carpetas de emuladores dentro de downloaded_media/
    emulador_dirs = [d for d in MEDIA_BASE_DIR.iterdir() if d.is_dir()]
    
    if not emulador_dirs:
        print(f"No se encontraron carpetas de emuladores dentro de '{MEDIA_BASE_DIR}'")
        return

    # Iterar sobre cada carpeta de emulador (ej: 'emulador1')
    for media_dir in emulador_dirs:
        emulador_name = media_dir.name
        batocera_name = obtener_nombre_batocera(emulador_name)
        
        print(f"\n## Procesando emulador: {emulador_name} -> {batocera_name}...")
        
        # --- TAREAS DE COPIA INVERSA ---
        
        # 1. MARQUEES (media/emulador1/marquees/juego1.png -> media-batocera/batocera_name/images/juego1-marquee.png)
        marquee_dir = media_dir / 'marquees'
        if marquee_dir.exists():
            patron_marquee = marquee_dir.glob('*.png')
            
            for origen_path in patron_marquee:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'images' / f'{game_name}-marquee.png'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/images/{game_name}-marquee.png")

        # 2. MIXIMAGES (media/emulador1/miximages/juego1.png -> media-batocera/batocera_name/media/images/juego1.png)
        miximages_dir = media_dir / 'miximages'
        if miximages_dir.exists():
            patron_mix = miximages_dir.glob('*.png')
            
            for origen_path in patron_mix:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'media' / 'images' / f'{game_name}.png'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/media/images/{game_name}.png")
            
        # 3. VIDEOS (media/emulador1/videos/juego1.mp4 -> media-batocera/batocera_name/media/video/juego1.mp4)
        videos_dir = media_dir / 'videos'
        if videos_dir.exists():
            patron_video = videos_dir.glob('*.mp4')
            
            for origen_path in patron_video:
                game_name = origen_path.stem
                destino_path = ROMS_BASE_DIR / batocera_name / 'media' / 'video' / f'{game_name}.mp4'
                total_copiados += copiar_fichero(origen_path, destino_path, f"{batocera_name}/media/video/{game_name}.mp4")

    # 4. Resumen final
    print("\n" + "=" * 50)
    print("Proceso de reversión finalizado.")
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
    revertir_archivos_multimedia()

    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
