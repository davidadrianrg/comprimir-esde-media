import sys
import shutil
import xml.etree.ElementTree as ET
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
#                   MODO DE SOBRESCRITURA
# -----------------------------------------------------------------
# Si es True, sobrescribirá los archivos gamelist.xml existentes en el destino.
# Si es False, omitirá el procesamiento de gamelist.xml que ya existen.
# NOTA: Los archivos multimedia (imágenes, videos) NUNCA se sobrescriben.
SOBRESCRIBIR_EXISTENTES = False

# -----------------------------------------------------------------
#          MAPEO DE SISTEMAS ES-DE → BATOCERA
# -----------------------------------------------------------------
# Diccionario que mapea los nombres de carpetas de ES-DE (key) 
# a los nombres correctos de Batocera (value)
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
    Usa el diccionario MAPEO_SISTEMAS (key=ES-DE, value=Batocera).
    Si no hay mapeo específico, devuelve None para omitir el sistema.
    """
    nombre_normalizado = nombre_esde.lower().strip()
    
    # Buscar directamente en el diccionario (key=ES-DE, value=Batocera)
    return MAPEO_SISTEMAS.get(nombre_normalizado, None)

# =================================================================
#                      FUNCIÓN DE COPIA
# =================================================================

def procesar_gamelist_xml(gamelist_origen: Path, gamelist_destino: Path, nombre_log: str) -> int:
    """
    Procesa un gamelist.xml de ES-DE y lo transforma al formato de Batocera.
    Modifica las rutas de image, video y añade el tag thumbnail.
    Retorna 1 si se procesó correctamente, 0 si hubo error o se omitió.
    """
    
    # Verificar si el archivo ya existe y no se permite sobreescritura
    if gamelist_destino.is_file() and not SOBRESCRIBIR_EXISTENTES:
        print(f"   [INFO] Ya existe: {nombre_log} - Omitiendo procesamiento.")
        return 0
    
    try:
        # Parsear el XML original
        tree = ET.parse(gamelist_origen)
        root = tree.getroot()
        
        # Procesar cada tag <game>
        juegos_procesados = 0
        for game in root.findall('game'):
            # Extraer nombre del juego del path para generar nombres de archivo
            path_elem = game.find('path')
            if path_elem is not None and path_elem.text:
                # Obtener nombre base del archivo sin extensión
                game_filename = Path(path_elem.text).stem
            else:
                # Si no hay path, usar un nombre genérico
                game_filename = f"game_{juegos_procesados}"
            
            # Procesar tag <image>
            image_elem = game.find('image')
            if image_elem is not None and image_elem.text:
                # Transformar: ./media/images/nombre.png -> ./images/nombre-image.png
                if image_elem.text.startswith('./media/images/'):
                    old_name = Path(image_elem.text).stem
                    image_elem.text = f'./images/{old_name}-image.png'
                elif image_elem.text.startswith('./images/'):
                    # Si ya tiene formato correcto, asegurar el sufijo -image
                    old_name = Path(image_elem.text).stem
                    if not old_name.endswith('-image'):
                        image_elem.text = f'./images/{old_name}-image.png'
            
            # Procesar tag <video>
            video_elem = game.find('video')
            if video_elem is not None and video_elem.text:
                # Transformar: ./media/videos/nombre.mp4 -> ./videos/nombre-video.mp4
                if video_elem.text.startswith('./media/videos/'):
                    old_name = Path(video_elem.text).stem
                    video_elem.text = f'./videos/{old_name}-video.mp4'
                elif video_elem.text.startswith('./videos/'):
                    # Si ya tiene formato correcto, asegurar el sufijo -video
                    old_name = Path(video_elem.text).stem
                    if not old_name.endswith('-video'):
                        video_elem.text = f'./videos/{old_name}-video.mp4'
            
            # Añadir tag <thumbnail> si no existe
            thumbnail_elem = game.find('thumbnail')
            if thumbnail_elem is None:
                # Crear nuevo elemento thumbnail
                thumbnail_elem = ET.SubElement(game, 'thumbnail')
                thumbnail_elem.text = f'./images/{game_filename}-thumb.png'
            elif thumbnail_elem.text:
                # Si existe, asegurar formato correcto
                if thumbnail_elem.text.startswith('./images/'):
                    old_name = Path(thumbnail_elem.text).stem
                    if not old_name.endswith('-thumb'):
                        thumbnail_elem.text = f'./images/{old_name}-thumb.png'
                else:
                    # Si tiene otro formato, convertirlo
                    old_name = Path(thumbnail_elem.text).stem
                    thumbnail_elem.text = f'./images/{old_name}-thumb.png'
            
            juegos_procesados += 1
        
        # Modo prueba: solo mostrar lo que se haría
        if MODO_PRUEBA:
            accion = "sobrescribiría" if gamelist_destino.is_file() else "procesaría y copiaría"
            print(f"   [PRUEBA] Se {accion}: {nombre_log} ({juegos_procesados} juegos)")
            return 1
        
        # Crear directorio destino si no existe
        gamelist_destino.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir el XML modificado manteniendo la declaración y encoding
        tree.write(
            gamelist_destino, 
            encoding='utf-8', 
            xml_declaration=True,
            method='xml'
        )
        
        accion = "sobrescrito" if gamelist_destino.is_file() else "procesado y copiado"
        print(f"   [{accion.upper()}] Exito al {accion}: {nombre_log} ({juegos_procesados} juegos)")
        return 1
        
    except ET.ParseError as e:
        print(f"   [ERROR] Error parseando XML {nombre_log}: {e}")
        return 0
    except Exception as e:
        print(f"   [ERROR] Error procesando {nombre_log}: {e}")
        return 0


def copiar_fichero(origen: Path, destino: Path, nombre_log: str):
    """
    Copia un archivo de origen a destino. 
    Maneja el modo de prueba y contabiliza la acción.
    NOTA: Los archivos multimedia NUNCA se sobrescriben para seguridad.
    """
    
    # 1. Crear el directorio de destino si no existe
    if not MODO_PRUEBA:
        destino.parent.mkdir(parents=True, exist_ok=True)

    # 2. Verificar si el archivo ya existe (los multimedia nunca se sobrescriben)
    if destino.is_file():
        print(f"   [INFO] Ya existe: {nombre_log} - Omitiendo copia.")
        return 0 # 0 archivos copiados

    # 3. Realizar o simular la copia
    if MODO_PRUEBA:
        print(f"   [PRUEBA] Se copiaría: {nombre_log}")
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
        modo_sobrescritura = "con sobreescritura" if SOBRESCRIBIR_EXISTENTES else "sin sobrescribir existentes"
        print(f"INICIANDO COPIA DE ARCHIVOS MULTIMEDIA Y PROCESAMIENTO DE GAMELISTS ({modo_sobrescritura}).")
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
            total_copiados += procesar_gamelist_xml(gamelist_origen, gamelist_destino, f"{batocera_name}/gamelist.xml")
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
