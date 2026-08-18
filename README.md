# Detectores Rn - Toma de datos

App para Android (hecha en Python con [Kivy](https://kivy.org)) para
registrar la colocación de detectores de radón, organizados por
**centros**, cada uno con sus **detectores** (plano, fotos y datos), y
generación de informe en PDF listo para enviar por WhatsApp.

Replica el esquema de la app de referencia (Base44 "Detectores Rn"):
centros con nombre/zona/fecha/imagen exterior, cada uno con varios
detectores colocados, e informe en PDF con selección de fotos a enviar.

## Esquema de la app

**Pantalla inicial — "Centros registrados"**
- Selector desplegable de centros grabados + botón **Abrir centro**.
- Lista de centros (nombre, zona, fecha), tocar uno lo abre directamente.
- **+ Crear nuevo centro**.
- Icono de ajustes (⚙): permite indicar el nombre del técnico/empresa
  que aparecerá en el PDF.

**Pantalla "Centro"**
- **Datos del centro**: nombre, zona, fecha de la medición, imagen
  exterior (con botón "Guardar cambios").
- **Detectores colocados**: lista de detectores (sala, planta, código),
  botón **Colocar nuevo detector**, y **Editar detectores** (activa un
  botón "Borrar" junto a cada detector).
- **Informe y envío**: botón **Generar PDF y enviar por WhatsApp**, y una
  lista de checkboxes para elegir qué fotos (exterior, planos, fotos de
  sala/detector) enviar junto con el PDF, con **Seleccionar todas**.

**Pantalla "Detector" (Nuevo / Editar)**
- **Datos del detector**: planta, sala, fecha, código del detector.
- **Plano de situación del detector**: subir o fotografiar el plano, y
  tocar sobre él para marcar un punto rojo con la ubicación exacta.
- **Fotografías**: imagen de la situación del detector, imagen del
  detector.
- **Cancelar** / **Guardar detector y salir**.

## Estructura del proyecto

```
radon_app/
├── main.py          # Lógica, base de datos, PDF y "compartir"
├── ui.kv            # Interfaz gráfica (3 pantallas)
├── buildozer.spec   # Configuración para compilar el APK con Buildozer
└── README.md
```

## Probar en el ordenador (sin Android)

```bash
pip install kivy pillow reportlab plyer
python3 main.py
```

En escritorio no hay cámara ni WhatsApp, así que:
- Al pedir una foto, se te preguntará "Tomar foto" o "Elegir de galería
  / archivo"; en el ordenador usa siempre la segunda opción.
- Al pulsar "Generar PDF y enviar por WhatsApp", como no hay integración
  de WhatsApp en escritorio, se te mostrará la ruta donde se ha guardado
  el PDF (y las fotos elegidas) en vez de abrirse el selector de
  aplicaciones.

## Compilar el APK para Android

Igual que antes: la compilación debe hacerse en **Linux** (nativo, WSL2,
o máquina virtual) con Buildozer, ya que descarga y usa el Android
SDK/NDK. No es posible generar el APK dentro de este chat.

1. Instala dependencias del sistema (Ubuntu/Debian):
   ```bash
   sudo apt update
   sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk \
       autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
       cmake libffi-dev libssl-dev
   ```

2. Instala Buildozer:
   ```bash
   pip3 install --user buildozer cython
   ```

3. Desde la carpeta del proyecto (`radon_app/`), compila el APK de
   depuración:
   ```bash
   buildozer -v android debug
   ```
   La primera vez tardará bastante porque descarga el Android SDK/NDK
   automáticamente. El APK resultante aparecerá en `bin/*.apk`.

4. Instala el APK en tu móvil (con depuración USB activada):
   ```bash
   buildozer android deploy run
   ```
   O copia el `.apk` de `bin/` al móvil y ábrelo para instalarlo.

### Alternativa sin instalar nada localmente

Puedes usar un flujo de **GitHub Actions** con la acción
[`ArtemSBulgakov/buildozer-action`](https://github.com/ArtemSBulgakov/buildozer-action):
subes el proyecto a un repositorio de GitHub, el workflow ejecuta
`buildozer android debug`, y descargas el APK como artefacto, sin
necesidad de un Linux propio.

## Notas técnicas

- **Base de datos**: SQLite con tres tablas — `centros` (nombre, zona,
  fecha, imagen exterior), `detectores` (uno por cada detector colocado,
  con `centro_id` como clave foránea, planta, sala, fecha, código,
  ruta del plano y coordenadas relativas 0–1 del punto marcado, y rutas
  de las dos fotos), y `settings` (nombre del técnico para el PDF).
- **Marcador en el plano**: igual que en la versión anterior, el widget
  `PlanoMarcador` traduce el toque en coordenadas relativas (0–1) de la
  imagen real (teniendo en cuenta el letterboxing), así que el punto
  queda en el sitio correcto sin importar el tamaño de pantalla.
- **"Sube o fotografía"**: cada botón de imagen (plano, fotos, imagen
  exterior) abre un pequeño selector con dos opciones — "Tomar foto"
  (cámara vía `plyer`) o "Elegir de galería / archivo" — igual que en
  la app de referencia.
- **PDF**: generado con `reportlab`. Incluye portada con los datos del
  centro y la imagen exterior, y una página por cada detector con sus
  datos, el plano con el punto "quemado" a resolución completa (con
  `Pillow`) y sus dos fotos.
- **Compartir por WhatsApp**: en Android se usa `plyer.share` para
  abrir el selector nativo de aplicaciones (donde WhatsApp aparece como
  una opción) con el PDF y, si se han marcado, las fotos seleccionadas
  —una detrás de otra, ya que compartir varios archivos como un único
  adjunto requeriría configuración nativa adicional de Android
  (`FileProvider` + intents personalizados) que no he podido verificar
  sin compilar y probar en un dispositivo real. Si te interesa esa
  versión más "todo en un solo mensaje", puedo prepararla, pero conviene
  probarla directamente en tu móvil según se vaya ajustando.
- Todas las imágenes (plano, fotos, imagen exterior) se copian al
  almacenamiento privado de la app nada más seleccionarlas, para que no
  se pierdan si el archivo original se mueve o se borra.

## Diferencias conocidas respecto a la app de referencia

- El selector de fecha es un campo de texto libre (`DD/MM/AAAA`), no un
  calendario nativo desplegable — Kivy no trae uno de serie. Si quieres,
  puedo añadir un selector de calendario simple.
- "Compartir por WhatsApp" envía el PDF y las fotos de una en una (ver
  nota técnica arriba) en vez de en un único paso "todo junto".
- No hay borrado de centros desde la pantalla inicial (solo de
  detectores, vía "Editar detectores"). Puedo añadirlo si lo necesitas.
