# Comprimir ES-DE Media

Conjunto de scripts Python para gestionar y optimizar archivos multimedia para EmulationStation-DE (ES-DE). Estos scripts ayudan a consolidar, optimizar y limpiar la colección de medios para retro gaming.

## 📋 Descripción de Scripts

### 1. `consolidar-media.py`
Consolida archivos multimedia desde diferentes directorios de origen a la estructura de carpetas de ES-DE.

**Funcionalidades:**
- Copia marquees desde `roms/emulador/images/*-marquee.png` a `media/emulador/marquees/`
- Copia miximages desde `roms/emulador/media/images/*.png` a `media/emulador/miximages/`
- Copia videos desde `roms/emulador/media/video/*.mp4` a `media/emulador/videos/`
- Modo de prueba seguro para previsualizar acciones antes de ejecutar
- No sobrescribe archivos existentes

### 2. `optimizar-imagenes.py`
Optimiza imágenes PNG reduciendo su tamaño mediante cuantización de colores.

**Funcionalidades:**
- Procesa imágenes en carpetas: `3dboxes`, `covers`, `marquees`, `miximages`, `screenshots`, `titlescreens`
- Reduce la paleta de colores a 256 colores (configurable)
- Mantiene la transparencia y optimiza la compresión
- Guarda las imágenes optimizadas en una carpeta separada
- Omite imágenes que ya existen en el destino para evitar reprocesamiento

### 3. `recortar-videos.py`
Recorta y comprime videos para reducir su tamaño y duración.

**Funcionalidades:**
- Recorta videos a los primeros 10 segundos (configurable)
- Comprime usando H.264 con CRF 28 (configurable)
- Convierte audio a AAC 128k
- Máxima compatibilidad con formato YUV420P
- Requiere FFmpeg instalado
- Omite videos que ya existen en el destino para evitar reprocesamiento

### 4. `comprobar-medios-faltantes.py`
Analiza todas las carpetas de emuladores y genera un reporte de medios faltantes.

**Funcionalidades:**
- Escanea todas las carpetas de emuladores en la carpeta `roms`
- Identifica todas las ROMs existentes (múltiples extensiones soportadas)
- Verifica la existencia de imágenes en: `3dboxes`, `covers`, `marquees`, `miximages`, `screenshots`, `titlescreens`
- Comprueba la existencia de videos en la carpeta `videos`
- Genera un archivo Excel por cada emulador con las ROMs que tienen medios faltantes
- Muestra estadísticas detalladas del análisis
- Formato de salida claro con indicadores visuales (❌ FALTA)

### 5. `remove-roms.py`
Elimina ROMs que no tienen imágenes de captura de pantalla correspondientes.

**Funcionalidades:**
- Busca ROMs con extensiones: `zip`, `7z`, `nes`, `sfc`, `n64`, `iso`, `cue`, `ccd`, `gdi`, `chd`, `m3u`, `rvz`, `dosz`, `cdi`, `dsk`, `cci`, `bin`, `pak`, `cso`, `scummvm`, `nsp`, `wua`
- Verifica existencia de imágenes PNG/JPG/JPEG en la carpeta `miximages`
- Modo de prueba seguro para previsualizar eliminaciones
- Limpia ROMs huérfanas sin medios asociados

## 🛠️ Requisitos

### Python
- Python 3.6 o superior

### Dependencias
```bash
pip install Pillow pandas openpyxl
```
- **Pillow**: Requerido para `optimizar-imagenes.py`
- **pandas**: Requerido para `comprobar-medios-faltantes.py`
- **openpyxl**: Requerido para `comprobar-medios-faltantes.py` (generación de Excel)

### Software Externo
- **FFmpeg** (requerido solo para `recortar-videos.py`)
  - Descargar desde: https://ffmpeg.org/download.html
  - Asegurarse de que esté en el PATH del sistema

## ⚙️ Configuración

Cada script tiene variables de configuración al principio que debes ajustar según tu sistema:

### Rutas Principales
```python
# Para consolidar-media.py y remove-roms.py
ROMS_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\roms')
MEDIA_BASE_DIR = Path('E:\\Documentos\\RetroGaming\\ES-DE\\ES-DE\\downloaded_media')

# Para optimizar-imagenes.py y recortar-videos.py
BASE_DIR = Path('E:\Documentos\RetroGaming\ES-DE\ES-DE\downloaded_media')
OUTPUT_DIR = Path('E:\Documentos\RetroGaming\ES-DE\ES-DE\downloaded_media_recortado')
```

### Modos de Seguridad
- **`MODO_PRUEBA`** (consolidar-media.py): `True` para simular, `False` para ejecutar
- **`EJECUTAR_BORRADO`** (remove-roms.py): `True` para borrar, `False` para simular

## 🚀 Uso

### 1. Consolidar Archivos Multimedia
```bash
python consolidar-media.py
```
Recomendación: Ejecuta primero con `MODO_PRUEBA = True` para verificar las acciones.

### 2. Optimizar Imágenes
```bash
python optimizar-imagenes.py
```
Las imágenes optimizadas se guardarán en la carpeta `downloaded_media_recortado`.

### 3. Recortar Videos
```bash
python recortar-videos.py
```
Asegúrate de tener FFmpeg instalado y en el PATH.

### 4. Comprobar Medios Faltantes
```bash
python comprobar-medios-faltantes.py
```
Generará un archivo Excel por cada emulador con las ROMs que tienen medios faltantes. Los archivos se nombran con el formato: `{emulador}_medios_faltantes_{timestamp}.xlsx`.

### 5. Limpiar ROMs sin Medios
```bash
python remove-roms.py
```
**ADVERTENCIA:** Ejecuta primero con `EJECUTAR_BORRADO = False` para revisar qué archivos se eliminarían.

## 📁 Estructura de Carpetas Esperada

```
RetroGaming/
├── roms/
│   ├── emulador1/
│   │   ├── juego1.zip
│   │   ├── images/
│   │   │   └── juego1-marquee.png
│   │   └── media/
│   │       ├── images/
│   │       │   └── juego1.png
│   │       └── video/
│   │           └── juego1.mp4
│   └── emulador2/
│       └── ...
└── ES-DE/
    └── ES-DE/
        └── downloaded_media/
            ├── emulador1/
            │   ├── marquees/
            │   ├── miximages/
            │   ├── videos/
            │   ├── covers/
            │   ├── screenshots/
            │   └── ...
            └── emulador2/
                └── ...
```

## ⚠️ Advertencias Importantes

1. **Respaldos:** Siempre realiza copias de seguridad de tus datos antes de ejecutar estos scripts.
2. **Modo Prueba:** Utiliza siempre los modos de prueba primero para verificar las acciones.
3. **FFmpeg:** Asegúrate de que FFmpeg esté correctamente instalado para el procesamiento de videos.
4. **Permisos:** Ejecuta los scripts con los permisos adecuados para acceder a las carpetas.

## 🔧 Personalización

### Optimización de Imágenes
Ajusta `NUM_COLORES` en `optimizar-imagenes.py`:
- `256`: Balance calidad/tamaño (recomendado)
- `128` o `64`: Mayor compresión, menor calidad

### Compresión de Video
Modifica estos parámetros en `recortar-videos.py`:
- `DURACION_SEGUNDOS`: Duración del recorte (default: 10)
- `CRF`: Calidad de video (23 = mejor, 28 = más pequeño)
- `PRESET`: Velocidad de codificación (fast, medium, slow)

### Extensiones de ROM
Edita `ROM_EXTENSIONS` en `remove-roms.py` para añadir o eliminar formatos.

## 🐛 Solución de Problemas

### Pillow no encontrado
```bash
pip install Pillow
```

### pandas o openpyxl no encontrados
```bash
pip install pandas openpyxl
```

### FFmpeg no encontrado
1. Descarga FFmpeg desde https://ffmpeg.org/download.html
2. Extrae los archivos
3. Añade la carpeta `bin` al PATH del sistema
4. Reinicia la terminal

### Rutas incorrectas
Verifica que las rutas en las variables de configuración correspondan a tu sistema:
- Usa barras dobles `\\` para Windows
- O usa `Path(r'C:\ruta\con\barras\normales')`

## 📄 Licencia

Este proyecto es de código abierto. Siéntete libre de modificarlo y distribuirlo según tus necesidades.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes sugerencias de mejora, por favor abre un issue o envía un pull request.
