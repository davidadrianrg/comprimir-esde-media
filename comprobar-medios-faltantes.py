import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

try:
    import pandas as pd
except ImportError:
    print("--- ERROR CRÍTICO ---")
    print("No se encontró la librería 'pandas'.")
    print("Por favor, instálala abriendo una terminal (CMD o PowerShell) y escribiendo:")
    print("pip install pandas openpyxl")
    # Pausa para que el usuario pueda leer el error
    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
    sys.exit(1)

# --- CONFIGURACIÓN ---

# 1. Ruta a la carpeta 'roms' principal (donde están las ROMs)
ROMS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\roms')

# 2. Ruta a la carpeta 'media' principal (donde están los medios)
MEDIA_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\downloaded_media')

# 3. Ruta a la carpeta de gamelists
GAMELISTS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\gamelists')

# 3. Lista de carpetas de imágenes a verificar
TARGET_FOLDERS = [
    '3dboxes', 
    'covers', 
    'marquees', 
    'miximages', 
    'screenshots', 
    'titlescreens',
    'videos'
]

# 4. Extensiones de archivos ROM a considerar (lista completa actualizada)
ROM_EXTENSIONS = {
    '.capcomorigins', '.zombies', '.0', '.000', '.0000', '.0001', '.001', '.015', '.017', '.018', '.019',
    '.01b', '.01f', '.01h', '.01j', '.01l', '.021', '.022', '.023', '.025', '.027', '.029', '.071',
    '.081', '.091', '.0a1', '.0n1', '.0x1', '.1', '.10', '.11', '.118', '.13', '.14', '.15', '.16',
    '.166', '.18', '.1976-0', '.2', '.26', '.29', '.2b4', '.3', '.386', '.4', '.49', '.5', '.50',
    '.51', '.6', '.62', '.67', '.68', '.7', '.7z', '.8', '.8769', '.88591', '.9', '.a', '.a1200',
    '.a500', '.a600', '.aac', '.abd', '.abr', '.abs', '.access', '.act', '.acv', '.ad', '.adc', '.adf',
    '.adt', '.adv', '.adx', '.afs', '.aifc', '.aix', '.alias', '.als', '.alt', '.ani', '.anm', '.ansi1251',
    '.apk', '.apm', '.appimage', '.aseprite', '.asm', '.asm_dx', '.asm_gl', '.asm_lbg', '.aspx', '.assets',
    '.ati', '.atlas', '.aud', '.auto', '.avi', '.avt', '.awd', '.bak', '.bank', '.bat', '.bfc', '.big5',
    '.big5@pinyin', '.big5@radical', '.big5@stroke', '.big5@zhuyin', '.big5hk', '.big5hk@radical',
    '.big5hk@stroke', '.big5hkscs', '.bin', '.bitmap', '.blend', '.blend1', '.bln', '.bmp', '.bmv', '.bnd',
    '.bnk', '.bpc', '.bph', '.bro', '.browser', '.bso', '.bun', '.c', '.cache', '.cadb', '.caf', '.cbc',
    '.cbs', '.ccd', '.cci', '.cdi', '.cdp', '.certs', '.cf', '.cfg', '.cfs', '.cfs_bk', '.cg', '.chd',
    '.chi', '.chips', '.chr', '.cib', '.cl3', '.cls', '.clu', '.clv', '.cmc', '.cmd', '.cmos', '.cnt',
    '.com', '.conf', '.config', '.cp1251', '.cp1255', '.cpl', '.cpp', '.cpt', '.crd', '.csb', '.csg', '.csh',
    '.cso', '.csp', '.css', '.csv', '.ctl', '.cur', '.cyrix', '.d', '.darwin', '.dat', '.dat0', '.dat1',
    '.data', '.db', '.ddb', '.dds', '.dectga', '.def', '.default', '.defaults', '.desktop', '.dig', '.dir',
    '.dll', '.dnr', '.doc', '.dosz', '.dps', '.drv', '.dsk', '.dtd', '.dxa', '.dylib', '.edg', '.edo',
    '.eeprom', '.efo', '.elf', '.en', '.enc', '.eng', '.enhancing', '.env', '.err', '.ess', '.ess_bk',
    '.euc', '.euc@dict', '.euc@pinyin', '.euc@radical', '.euc@stroke', '.euc@zhuyin', '.eucjp', '.euckr',
    '.euctw', '.exe', '.exp', '.f3dex2e', '.farc', '.fdt', '.fgd', '.file', '.fit', '.fla', '.flu',
    '.fnt', '.fon', '.fonts', '.fp', '.frag', '.ftg', '.fx', '.fxb', '.gal', '.game', '.gb18030',
    '.gb18030@pinyin', '.gb18030@radical', '.gb18030@stroke', '.gb2312', '.gbk', '.gbk@pinyin', '.gbk@radical',
    '.gbk@stroke', '.gbs', '.gcz', '.georgianps', '.gid', '.gif', '.gl', '.glb', '.glsl', '.glslp', '.gme',
    '.gra', '.grf', '.gst', '.gz', '.h', '.hashdb', '.hd', '.hdf', '.help', '.hi', '.highs', '.hlp',
    '.hmf', '.htm', '.html', '.i128', '.i740', '.i810', '.ia1', '.ia16', '.ia4', '.ia8', '.ibk', '.ibl',
    '.icns', '.ico', '.id', '.idb', '.idx', '.ims', '.in', '.inc', '.inf', '.info', '.ini', '.ini~',
    '.inl', '.ipd', '.iso', '.iso-8859-1', '.iso8859-1', '.iso8859-11', '.iso8859-13', '.iso8859-15',
    '.iso8859-1@bokmal', '.iso8859-1@nynorsk', '.iso8859-2', '.iso8859-2@bosnia', '.iso8859-5',
    '.iso8859-6', '.iso8859-7', '.iso8859-7@euro', '.iso8859-8', '.iso8859-9', '.iso88591', '.iso885913',
    '.iso885914', '.iso885915', '.iso885915@euro', '.iso88592', '.iso88593', '.iso88595', '.iso88595@cyrillic',
    '.iso88596', '.iso88597', '.iso88598', '.iso88599', '.iso_8859-1', '.it', '.ja', '.jam', '.jar',
    '.jennifer', '.jpeg', '.jpg', '.js', '.json', '.key', '.keys', '.ko', '.koi8-r', '.koi8r', '.koi8t',
    '.koi8u', '.la', '.la0', '.la1', '.la2', '.ldci', '.lec', '.lfl', '.lha', '.library', '.list', '.lit',
    '.lm', '.lna', '.lng', '.lng-', '.lnk', '.lnm', '.lno', '.lnu', '.lnv', '.lock', '.log', '.lsp',
    '.lss', '.lss_bk', '.lst', '.lta', '.ltm', '.lto', '.ltu', '.ltv', '.lua', '.luac', '.lvl', '.lvlx',
    '.lvm', '.lynxos', '.m2v', '.m3u', '.m4a', '.m64', '.map', '.mbi', '.md', '.md3', '.mdb', '.mdi',
    '.me', '.mgfxo', '.mhtml', '.mid', '.mix', '.mk', '.mlg', '.mouse', '.mp3', '.mp4', '.mpd', '.msu',
    '.mus', '.mx2map', '.mx2palette', '.n64', '.nam', '.nes', '.net', '.netbsd', '.new', '.newport', '.nls',
    '.notes', '.nsf', '.nsp', '.nut', '.nut_bk', '.nutc', '.nvmem', '.nvr', '.o', '.o2r', '.ogg', '.oni',
    '.openbsd', '.opl', '.orb', '.org', '.otf', '.otr', '.out', '.p', '.pa4', '.pa8', '.pac', '.pack',
    '.pak', '.pal', '.pas', '.pbn', '.pbp', '.pc', '.pcf', '.pck', '.pcm', '.pcx', '.pdb', '.pdf', '.pdn',
    '.pf', '.pif', '.pk2', '.pk3', '.pl', '.pmf', '.png', '.policy', '.poly', '.pov', '.ppdb', '.prefs',
    '.prev', '.prf', '.properties', '.ps', '.psd', '.psn', '.ptp', '.py', '.r128', '.rapidaccess', '.rar',
    '.rb', '.rcf', '.rcss', '.re_', '.readme', '.real', '.reapeaks', '.rec', '.rendition', '.res',
    '.resource', '.ress', '.rev', '.rfo', '.rfz', '.rgba16', '.rgssad', '.rif', '.rip', '.rml', '.rpc',
    '.rs', '.rsc', '.rtb', '.rtc', '.rtz', '.rules', '.rvz', '.rxdata', '.s01', '.s3virge', '.sample',
    '.san', '.sav', '.save', '.sbi', '.sbk', '.scale', '.scn', '.sco', '.scr', '.scummvm', '.security',
    '.seq', '.set', '.sfc', '.sfd', '.sfk', '.sfx', '.sh', '.shlib', '.shp', '.sis', '.sjis', '.smk',
    '.smp', '.so', '.sog', '.solaris', '.son', '.sou', '.spc', '.spd', '.squbin', '.sram', '.src', '.srm',
    '.sss', '.std', '.style', '.sup', '.sv', '.svg', '.svg_', '.svl', '.svm', '.tab', '.table', '.tat',
    '.tbl', '.tcvn', '.template', '.termcap', '.terminfo', '.tfd', '.tft', '.tga', '.tgt', '.tic',
    '.tis620', '.tlk', '.tmp', '.tmpl', '.trs', '.tsk', '.ttf', '.twmrc', '.txt', '.txt~', '.uae',
    '.uc', '.ujis', '.unx', '.url', '.utf-8', '.utf-8@dict', '.utf-8@pinyin', '.utf-8@radical',
    '.utf-8@stroke', '.utf-8@zhuyin', '.utf8', '.uva', '.uze', '.vbs', '.vert', '.vga', '.vlp', '.voc',
    '.vp', '.vpx', '.vxd', '.wad', '.wav', '.wbfs', '.win', '.wldx', '.wnd', '.wri', '.wsquashfs',
    '.wua', '.x86', '.x86_64', '.xaf', '.xbel', '.xbm', '.xbox360', '.xcf', '.xgs', '.xkb-config',
    '.xkb-enhancing', '.xls', '.xml', '.xmp', '.xnb', '.xpm', '.xpr', '.xsb', '.xsm', '.xwb', '.yaml',
    '.ybo', '.yml', '.ynabin', '.ynasqu', '.z64', '.zip', '.zpbn', '.zscript', '.zspr', '.zxnb'
}

# 5. Nombre del archivo Excel de salida
OUTPUT_EXCEL = 'reporte_medios_faltantes.xlsx'

# --- FIN DE LA CONFIGURACIÓN ---


def cargar_gamelist(emulador_name: str) -> dict:
    """
    Carga el gamelist.xml de un emulador y retorna un diccionario
    con nombre_archivo -> nombre_juego.
    """
    gamelist_path = GAMELISTS_BASE_DIR / f'{emulador_name}' / 'gamelist.xml'
    
    if not gamelist_path.exists():
        print(f"   📋 No se encontró gamelist.xml para {emulador_name}")
        return {}
    
    try:
        tree = ET.parse(gamelist_path)
        root = tree.getroot()
        
        gamelist_dict = {}
        for game in root.findall('game'):
            path_elem = game.find('path')
            name_elem = game.find('name')
            
            if path_elem is not None and name_elem is not None:
                # Extraer el nombre del archivo del path (ej: ./sf2hf.7z -> sf2hf.7z)
                path_text = path_elem.text
                if path_text.startswith('./'):
                    filename = path_text[2:]  # Quitar './'
                else:
                    filename = path_text
                
                # Obtener el nombre base sin extensión para comparación
                base_name = Path(filename).stem
                gamelist_dict[base_name] = name_elem.text
                gamelist_dict[filename] = name_elem.text  # También guardar con extensión
        
        print(f"   📋 Cargados {len(gamelist_dict)} juegos desde gamelist.xml")
        return gamelist_dict
        
    except Exception as e:
        print(f"   ❌ Error al cargar gamelist.xml para {emulador_name}: {e}")
        return {}


def obtener_lista_roms(emulador_dir: Path) -> list:
    """
    Obtiene una lista de todas las ROMs en un directorio de emulador.
    Retorna una lista de tuplas (nombre_base, ruta_completa).
    """
    roms = []
    
    # Buscar archivos con las extensiones especificadas
    for ext in ROM_EXTENSIONS:
        for rom_file in emulador_dir.glob(f'*{ext}'):
            # Obtener el nombre base sin extensión
            nombre_base = rom_file.stem
            roms.append((nombre_base, rom_file))
    
    return roms


def verificar_medios_faltantes(nombre_rom: str, emulador_name: str) -> dict:
    """
    Verifica qué medios faltan para una ROM específica.
    Retorna un diccionario con los medios faltantes.
    """
    faltantes = {}
    
    # Verificar carpetas de imágenes (excluyendo 'videos' que se maneja por separado)
    for folder in TARGET_FOLDERS:
        if folder == 'videos':
            continue
        media_path = MEDIA_BASE_DIR / emulador_name / folder / f'{nombre_rom}.png'
        if not media_path.exists():
            faltantes[folder] = f'Falta {folder}'
    
    # Verificar video
    video_path = MEDIA_BASE_DIR / emulador_name / 'videos' / f'{nombre_rom}.mp4'
    if not video_path.exists():
        faltantes['video'] = 'Falta video'
    
    return faltantes


def generar_reporte_excel(datos_reporte: dict, filename: str):
    """
    Genera un archivo Excel con el reporte de medios faltantes para todos los emuladores.
    datos_reporte: diccionario {emulador_name: lista_datos}
    """
    if not datos_reporte:
        print("No hay medios faltantes para ningún emulador")
        return
    
    try:
        # Crear writer de Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            total_faltantes = 0
            
            for emulador_name, datos in datos_reporte.items():
                if not datos:
                    # Si no hay datos, crear una hoja vacía con un mensaje
                    df_vacio = pd.DataFrame({'Mensaje': [f'No hay medios faltantes para {emulador_name}']})
                    df_vacio.to_excel(writer, sheet_name=emulador_name[:31], index=False)  # Limitar nombre de hoja a 31 chars
                    continue
                
                # Crear DataFrame para este emulador
                df = pd.DataFrame(datos)
                
                # Reordenar columnas para mejor visualización
                columnas_orden = ['ROM', 'Nombre Juego', 'Ruta ROM'] + [col for col in df.columns if col not in ['ROM', 'Nombre Juego', 'Ruta ROM']]
                df = df[columnas_orden]
                
                # Escribir en la hoja del emulador (limitar nombre a 31 caracteres para Excel)
                sheet_name = emulador_name[:31] if len(emulador_name) > 31 else emulador_name
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Ajustar ancho de columnas
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)  # Máximo 50 caracteres
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                total_faltantes += len(datos)
                print(f"   ✅ Hoja '{sheet_name}' creada con {len(datos)} ROMs con medios faltantes")
        
        print(f"\n📊 Reporte Excel generado: {filename}")
        print(f"   Total de ROMs con medios faltantes: {total_faltantes}")
        print(f"   Total de emuladores procesados: {len(datos_reporte)}")
        
    except Exception as e:
        print(f"❌ Error al generar el archivo Excel: {e}")


def comprobar_medios_emulador(emulador_dir: Path):
    """
    Comprueba medios faltantes para un emulador específico.
    Retorna los datos para el reporte.
    """
    emulador_name = emulador_dir.name
    print(f"\n🎮 Analizando emulador: {emulador_name}")
    print("-" * 50)
    
    # 1. Cargar gamelist.xml
    gamelist_dict = cargar_gamelist(emulador_name)
    
    # 2. Obtener lista de ROMs
    roms = obtener_lista_roms(emulador_dir)
    
    if not roms:
        print(f"   No se encontraron ROMs en: {emulador_dir}")
        return emulador_name, []
    
    print(f"   Encontradas {len(roms)} ROMs")
    
    # 3. Verificar medios para cada ROM
    datos_reporte = []
    total_con_faltantes = 0
    total_en_gamelist = 0
    
    for i, (nombre_rom, ruta_rom) in enumerate(roms, 1):
        print(f"   [{i}/{len(roms)}] Verificando: {nombre_rom}")
        
        # Verificar si está en el gamelist
        nombre_juego = gamelist_dict.get(nombre_rom, "❌ NO EN GAMELIST")
        if nombre_juego != "❌ NO EN GAMELIST":
            total_en_gamelist += 1
        
        faltantes = verificar_medios_faltantes(nombre_rom, emulador_name)
        
        # Agregar siempre si faltan medios O si no está en gamelist
        if faltantes or nombre_juego == "❌ NO EN GAMELIST":
            if faltantes:
                total_con_faltantes += 1
            
            # Preparar fila para el reporte
            fila = {
                'ROM': nombre_rom,
                'Nombre Juego': nombre_juego,
                'Ruta ROM': str(ruta_rom.relative_to(ROMS_BASE_DIR))
            }
            
            # Agregar cada medio faltante como columna
            for medio, descripcion in faltantes.items():
                fila[medio] = '❌ FALTA'
            
            # Agregar columna de gamelist si no está
            if nombre_juego == "❌ NO EN GAMELIST":
                fila['En GameList'] = '❌ NO'
            
            datos_reporte.append(fila)
    
    print(f"\n   📊 Resumen:")
    print(f"   - Total ROMs analizadas: {len(roms)}")
    print(f"   - ROMs en gamelist.xml: {total_en_gamelist}")
    print(f"   - ROMs con medios faltantes: {total_con_faltantes}")
    print(f"   - ROMs completas: {len(roms) - total_con_faltantes}")
    
    if not datos_reporte:
        print("   🎉 ¡Todas las ROMs tienen sus medios completos y están en el gamelist!")
    
    return emulador_name, datos_reporte


def comprobar_medios_faltantes():
    """
    Función principal que ejecuta la comprobación de medios faltantes.
    """
    print("🔍 INICIANDO COMPROBACIÓN DE MEDIOS FALTANTES")
    print("=" * 60)
    
    # 1. Validar carpetas base
    if not ROMS_BASE_DIR.is_dir():
        print(f"❌ Error: No se encontró la carpeta de ROMs: '{ROMS_BASE_DIR.resolve()}'")
        print("   Asegúrate de que la ruta en ROMS_BASE_DIR sea correcta.")
        return
    
    if not MEDIA_BASE_DIR.is_dir():
        print(f"❌ Error: No se encontró la carpeta de medios: '{MEDIA_BASE_DIR.resolve()}'")
        print("   Asegúrate de que la ruta en MEDIA_BASE_DIR sea correcta.")
        return
    
    print(f"📁 Carpeta de ROMs: {ROMS_BASE_DIR.resolve()}")
    print(f"📁 Carpeta de medios: {MEDIA_BASE_DIR.resolve()}")
    print(f"🎯 Carpetas de imágenes a verificar: {', '.join([f for f in TARGET_FOLDERS if f != 'videos'])}")
    print(f"🎬 También se verificará la carpeta 'videos'")
    
    # 2. Buscar carpetas de emuladores
    emulador_dirs = [d for d in ROMS_BASE_DIR.iterdir() if d.is_dir()]
    
    if not emulador_dirs:
        print(f"\n❌ No se encontraron carpetas de emuladores en: {ROMS_BASE_DIR}")
        return
    
    print(f"\n🎮 Encontrados {len(emulador_dirs)} emuladores:")
    for emulador_dir in emulador_dirs:
        print(f"   - {emulador_dir.name}")
    
    # 3. Analizar cada emulador y acumular datos
    datos_totales = {}
    
    for emulador_dir in emulador_dirs:
        try:
            emulador_name, datos_emulador = comprobar_medios_emulador(emulador_dir)
            datos_totales[emulador_name] = datos_emulador
        except Exception as e:
            print(f"❌ Error al procesar el emulador {emulador_dir.name}: {e}")
            continue
    
    # 4. Generar reporte Excel único con todos los datos
    if datos_totales:
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_medios_faltantes_{timestamp}.xlsx"
        
        print(f"\n📝 Generando reporte Excel consolidado...")
        generar_reporte_excel(datos_totales, filename)
    else:
        print("\n❌ No se pudieron procesar los datos de ningún emulador")
    
    print("\n" + "=" * 60)
    print("✅ COMPROBACIÓN DE MEDIOS FALTANTES FINALIZADA")
    print("=" * 60)


# --- Punto de entrada principal ---
if __name__ == "__main__":
    # La comprobación de pandas se hace al inicio con el 'try...except ImportError'
    comprobar_medios_faltantes()
    
    # Pausa al final en Windows si se hace doble clic
    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
