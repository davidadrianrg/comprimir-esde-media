import sys
from pathlib import Path
import pandas as pd
import os

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
#                   NUEVAS FUNCIONES EXCEL
# =================================================================

def leer_excel_medios_faltantes(ruta_excel):
    """
    Lee el archivo Excel de medios faltantes y retorna un DataFrame
    con todos los datos consolidados de todas las hojas.
    """
    try:
        # Verificar que el archivo existe
        if not Path(ruta_excel).exists():
            print(f"❌ Error: No se encuentra el archivo Excel en: {ruta_excel}")
            return None
        
        print(f"📖 Leyendo archivo Excel: {ruta_excel}")
        
        # Leer todas las hojas del Excel
        excel_file = pd.ExcelFile(ruta_excel)
        todos_los_datos = []
        
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(ruta_excel, sheet_name=sheet_name)
                
                # Ignorar hojas vacías o con mensajes
                if df.empty or 'Mensaje' in df.columns:
                    continue
                
                # Agregar columna con el nombre del emulador (hoja)
                df['Emulador'] = sheet_name
                todos_los_datos.append(df)
                
                print(f"   ✅ Hoja '{sheet_name}': {len(df)} ROMs con problemas")
                
            except Exception as e:
                print(f"   ⚠️ Error al leer hoja '{sheet_name}': {e}")
                continue
        
        if not todos_los_datos:
            print("❌ No se encontraron datos válidos en el archivo Excel")
            return None
        
        # Combinar todos los datos
        df_consolidado = pd.concat(todos_los_datos, ignore_index=True)
        print(f"📊 Total de ROMs con problemas: {len(df_consolidado)}")
        
        return df_consolidado
        
    except Exception as e:
        print(f"❌ Error al leer el archivo Excel: {e}")
        return None


def mostrar_menu_opciones():
    """
    Muestra el menú interactivo de opciones y retorna la selección del usuario.
    """
    print("\n" + "=" * 60)
    print("🎮 MENÚ DE OPCIONES DE BORRADO")
    print("=" * 60)
    print("1. 🗑️  Borrar TODOS los juegos con algún medio faltante")
    print("2. 📋 Borrar SOLO los juegos que NO están en la gamelist")
    print("3. ❌ Salir sin borrar nada")
    print("-" * 60)
    
    while True:
        try:
            opcion = input("Selecciona una opción (1-3): ").strip()
            if opcion in ['1', '2', '3']:
                return int(opcion)
            else:
                print("❌ Opción no válida. Por favor, selecciona 1, 2 o 3.")
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")


def filtrar_roms_segun_opcion(df_datos, opcion):
    """
    Filtra las ROMs según la opción seleccionada por el usuario.
    Retorna una lista de diccionarios con la información de las ROMs a borrar.
    """
    roms_a_borrar = []
    
    if opcion == 1:
        # Opción 1: Borrar todos los juegos con algún medio faltante
        print("\n🔍 Filtrando: TODOS los juegos con algún medio faltante...")
        
        # Buscar filas que tengan algún medio faltante (columnas con "❌ FALTA")
        columnas_medios = ['3dboxes', 'covers', 'marquees', 'miximages', 'screenshots', 'titlescreens', 'video']
        
        for _, row in df_datos.iterrows():
            tiene_medio_faltante = False
            for medio in columnas_medios:
                if medio in row and pd.notna(row[medio]) and '❌ FALTA' in str(row[medio]):
                    tiene_medio_faltante = True
                    break
            
            if tiene_medio_faltante:
                roms_a_borrar.append({
                    'rom': row['ROM'],
                    'nombre_juego': row['Nombre Juego'],
                    'ruta_relativa': row['Ruta ROM'],
                    'emulador': row['Emulador'],
                    'motivo': 'Medios faltantes'
                })
    
    elif opcion == 2:
        # Opción 2: Borrar solo los que no están en la gamelist
        print("\n🔍 Filtrando: SOLO juegos que NO están en la gamelist...")
        
        for _, row in df_datos.iterrows():
            if 'Nombre Juego' in row and pd.notna(row['Nombre Juego']) and '❌ NO EN GAMELIST' in str(row['Nombre Juego']):
                roms_a_borrar.append({
                    'rom': row['ROM'],
                    'nombre_juego': row['Nombre Juego'],
                    'ruta_relativa': row['Ruta ROM'],
                    'emulador': row['Emulador'],
                    'motivo': 'No está en gamelist'
                })
    
    return roms_a_borrar


def mostrar_resumen_borrado(roms_a_borrar):
    """
    Muestra un resumen detallado de las ROMs que se van a borrar.
    """
    if not roms_a_borrar:
        print("\n✅ No hay ROMs que cumplan los criterios seleccionados.")
        return False
    
    print(f"\n📋 RESUMEN DE ROMS A BORRAR: {len(roms_a_borrar)}")
    print("=" * 80)
    
    # Agrupar por emulador
    por_emulador = {}
    for rom in roms_a_borrar:
        emulador = rom['emulador']
        if emulador not in por_emulador:
            por_emulador[emulador] = []
        por_emulador[emulador].append(rom)
    
    for emulador, roms in por_emulador.items():
        print(f"\n🎮 {emulador}: {len(roms)} ROMs")
        print("-" * 40)
        for i, rom in enumerate(roms[:10], 1):  # Mostrar solo las primeras 10
            print(f"   {i:2d}. {rom['rom']} ({rom['motivo']})")
        
        if len(roms) > 10:
            print(f"   ... y {len(roms) - 10} más")
    
    print(f"\n⚠️  TOTAL: {len(roms_a_borrar)} ROMs serán eliminadas")
    return True


def borrar_roms_desde_excel(roms_a_borrar):
    """
    Borra las ROMs físicamente usando las rutas del Excel.
    """
    if not EJECUTAR_BORRADO:
        print("\n⚠️ MODO DE PRUEBA ACTIVADO. No se borrará ningún archivo. ⚠️")
        print("Para borrar archivos, cambia 'EJECUTAR_BORRADO' a True en el script.")
        print("-" * 50)
    
    total_borradas = 0
    total_errores = 0
    
    for rom in roms_a_borrar:
        # Construir la ruta completa de la ROM
        ruta_completa = ROMS_BASE_DIR / rom['ruta_relativa']
        
        if not ruta_completa.exists():
            print(f"   [ERROR] 🚫 No existe: {ruta_completa}")
            total_errores += 1
            continue
        
        if EJECUTAR_BORRADO:
            try:
                ruta_completa.unlink()  # Borra el archivo
                print(f"   [BORRADO] 🗑️ Eliminado: {rom['rom']} ({rom['emulador']})")
                total_borradas += 1
            except Exception as e:
                print(f"   [ERROR] ❌ No se pudo borrar {rom['rom']}: {e}")
                total_errores += 1
        else:
            print(f"   [PRUEBA] 🚫 Se borraría: {rom['rom']} ({rom['emulador']})")
            total_borradas += 1
    
    return total_borradas, total_errores


def buscar_archivo_excel():
    """
    Busca automáticamente el archivo Excel más reciente de medios faltantes.
    """
    print("🔍 Buscando archivo Excel de medios faltantes...")
    
    # Buscar archivos que coincidan con el patrón
    archivos_excel = list(Path('.').glob('reporte_medios_faltantes_*.xlsx'))
    
    if not archivos_excel:
        print("❌ No se encontraron archivos Excel de medios faltantes en el directorio actual.")
        return None
    
    # Ordenar por fecha de modificación (el más reciente primero)
    archivos_excel.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print("📁 Archivos Excel encontrados:")
    for i, archivo in enumerate(archivos_excel[:5], 1):  # Mostrar los 5 más recientes
        fecha_mod = archivo.stat().st_mtime
        fecha_formateada = pd.to_datetime(fecha_mod, unit='s').strftime('%Y-%m-%d %H:%M:%S')
        print(f"   {i}. {archivo.name} (modificado: {fecha_formateada})")
    
    # Usar el más reciente automáticamente
    archivo_seleccionado = archivos_excel[0]
    print(f"\n✅ Seleccionado automáticamente: {archivo_seleccionado.name}")
    
    return str(archivo_seleccionado)


# =================================================================
#                   FUNCIÓN PRINCIPAL MODIFICADA
# =================================================================

def limpiar_roms_desde_excel():
    """
    Función principal que lee el Excel de medios faltantes y permite borrar ROMs
    según los criterios seleccionados por el usuario.
    """
    print("🎮 LIMPIEZA DE ROMS DESDE EXCEL DE MEDIOS FALTANTES")
    print("=" * 60)
    
    # 1. Buscar archivo Excel
    ruta_excel = buscar_archivo_excel()
    if not ruta_excel:
        # Si no se encuentra automáticamente, pedir al usuario
        ruta_excel = input("\n📂 Ingresa la ruta del archivo Excel de medios faltantes: ").strip()
        if not ruta_excel or not Path(ruta_excel).exists():
            print("❌ No se proporcionó una ruta válida. Saliendo...")
            return
    
    # 2. Leer el Excel
    df_datos = leer_excel_medios_faltantes(ruta_excel)
    if df_datos is None:
        print("❌ No se pudieron leer los datos del Excel. Saliendo...")
        return
    
    # 3. Mostrar menú de opciones
    opcion = mostrar_menu_opciones()
    
    if opcion == 3:
        print("👋 Saliendo sin realizar cambios.")
        return
    
    # 4. Filtrar ROMs según opción
    roms_a_borrar = filtrar_roms_segun_opcion(df_datos, opcion)
    
    # 5. Mostrar resumen
    if not mostrar_resumen_borrado(roms_a_borrar):
        return
    
    # 6. Confirmación final
    if not EJECUTAR_BORRADO:
        print("\n📝 MODO DE PRUEBA: No se realizará ningún borrado real.")
    else:
        print("\n⚠️ ¡ADVERTENCIA! Estás a punto de borrar archivos reales.")
        confirmacion = input("¿Estás seguro de continuar? (escribe 'BORRAR' para confirmar): ").strip().upper()
        if confirmacion != 'BORRAR':
            print("❌ Operación cancelada por el usuario.")
            return
    
    # 7. Ejecutar borrado
    print(f"\n🔥 {'EJECUTANDO' if EJECUTAR_BORRADO else 'SIMULANDO'} BORRADO...")
    print("-" * 50)
    
    total_borradas, total_errores = borrar_roms_desde_excel(roms_a_borrar)
    
    # 8. Resumen final
    print("\n" + "=" * 60)
    print("✨ Tarea de limpieza finalizada.")
    print(f"ROMs {'borradas' if EJECUTAR_BORRADO else 'procesadas'}: {total_borradas}")
    if total_errores > 0:
        print(f"Errores encontrados: {total_errores}")
    print("=" * 60)


def limpiar_roms_sin_media():
    """Función original: Busca roms que no tienen una imagen de captura de pantalla correspondiente (PNG o JPG)."""
    
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
    print("🎮 ELIGE EL MODO DE OPERACIÓN:")
    print("=" * 40)
    print("1. 📊 Borrar ROMs desde Excel de medios faltantes (NUEVO)")
    print("2. 🔍 Borrar ROMs sin imágenes (Método original)")
    print("-" * 40)
    
    try:
        modo = input("Selecciona un modo (1-2): ").strip()
        if modo == "1":
            limpiar_roms_desde_excel()
        elif modo == "2":
            limpiar_roms_sin_media()
        else:
            print("❌ Opción no válida. Saliendo...")
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")

    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
