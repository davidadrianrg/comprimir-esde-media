import subprocess
from pathlib import Path
import sys

# --- CONFIGURACIÓN ---

# 1. Ruta a la carpeta 'media' principal
#    El script espera encontrar esta carpeta en el mismo lugar donde se ejecuta.
#    O puedes poner la ruta completa, ej: Path('C:/Users/TuUsuario/Videos/media')
BASE_DIR = Path('E:\Documentos\RetroGaming\ES-DE\ES-DE\downloaded_media')

# 2. Nombre de la carpeta donde se guardarán los videos nuevos
OUTPUT_DIR = Path('E:\Documentos\RetroGaming\ES-DE\ES-DE\downloaded_media_recortado')

# 3. Duración del recorte (en segundos)
DURACION_SEGUNDOS = '10'

# 4. Configuración de compresión (para FFmpeg)
#    -crf (Constant Rate Factor): La calidad. 
#          Un número MÁS ALTO significa MENOS calidad y archivo MÁS PEQUEÑO.
#          '23' es un buen balance. '28' es más pequeño.
CRF = '28' 
#    -preset: Velocidad de codificación.
#          'medium' es el default. 'fast' o 'faster' irán más rápido
#          a costa de un poco de eficiencia de compresión.
PRESET = 'fast'
#    -b:a (Audio Bitrate): Calidad del audio.
AUDIO_BITRATE = '128k'

# --- FIN DE LA CONFIGURACIÓN ---


def verificar_ffmpeg():
    """Comprueba si FFmpeg está instalado y en el PATH."""
    try:
        subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            check=True, 
            encoding='utf-8'
        )
        return True
    except FileNotFoundError:
        print("--- ERROR CRÍTICO ---")
        print("No se encontró 'ffmpeg'. Por favor, instálalo y asegúrate de")
        print("que esté añadido al PATH de tu sistema.")
        print("Descarga desde: https://ffmpeg.org/download.html")
        return False
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg parece estar instalado, pero dio un error: {e.stderr}")
        return False

def procesar_videos():
    """Encuentra y procesa todos los videos."""
    
    # 1. Validar la carpeta de entrada
    if not BASE_DIR.is_dir():
        print(f"Error: No se encontró la carpeta de entrada: '{BASE_DIR.resolve()}'")
        print("Asegúrate de que el script esté en el lugar correcto o ajusta BASE_DIR.")
        return

    # 2. Encontrar todos los videos que coincidan con el patrón
    #    media/CUALQUIER_COSA/videos/CUALQUIER_COSA.mp4
    patron_busqueda = '*/videos/*.mp4'
    video_files = list(BASE_DIR.glob(patron_busqueda))

    if not video_files:
        print(f"No se encontraron videos .mp4 con la estructura '{BASE_DIR}/{patron_busqueda}'")
        return

    print(f"Encontrados {len(video_files)} videos. Procesando...")
    print(f"Los resultados se guardarán en: '{OUTPUT_DIR.resolve()}'")

    # 3. Procesar cada video
    for i, video_path in enumerate(video_files):
        
        # 4. Calcular la ruta de salida
        #    Ej: media/emulador1/videos/video1.mp4
        #        -> media_recortado/emulador1/videos/video1.mp4
        relative_path = video_path.relative_to(BASE_DIR)
        output_path = OUTPUT_DIR / relative_path

        # 5. Verificar si el archivo ya existe
        if output_path.is_file():
            print(f"\n[{i+1}/{len(video_files)}] Omitiendo: {video_path.name}")
            print(f"  -> Ya existe en: {output_path}")
            continue

        # 6. Crear el directorio de salida si no existe
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n[{i+1}/{len(video_files)}] Procesando: {video_path.name}")
        print(f"  -> Guardando en: {output_path}")

        # 7. Construir el comando de FFmpeg
        command = [
            'ffmpeg',
            '-i', str(video_path),     # Archivo de entrada
            '-t', DURACION_SEGUNDOS,   # Duración (trim)
            '-c:v', 'libx264',         # Códec de video (H.264, muy compatible)
            '-crf', CRF,               # Calidad de video
            '-preset', PRESET,         # Velocidad de codificación
            '-c:a', 'aac',             # Códec de audio (AAC, muy compatible)
            '-b:a', AUDIO_BITRATE,     # Calidad de audio
            '-pix_fmt', 'yuv420p',     # Formato de píxeles para máxima compatibilidad
            str(output_path)           # Archivo de salida
        ]

        # 8. Ejecutar el comando
        try:
            # capture_output=True esconde la salida de ffmpeg a menos que haya un error
            subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            print(f"  [ÉXITO] Video recortado y codificado.")
        
        except subprocess.CalledProcessError as e:
            # Si FFmpeg falla, muestra el error
            print(f"  [ERROR] Falló el procesamiento de {video_path.name}:")
            print("--- Salida de error de FFmpeg ---")
            print(e.stderr)
            print("---------------------------------")
        
    print("\n¡Proceso completado!")

# --- Punto de entrada principal ---
if __name__ == "__main__":
    if verificar_ffmpeg():
        procesar_videos()
    
    # Pausa al final en Windows si se hace doble clic
    if sys.platform == "win32":
        input("\nPresiona Enter para salir...")
