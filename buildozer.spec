[app]

# (str) Título de la app
title = Detectores Rn

# (str) Nombre del paquete
package.name = radondata

# (str) Dominio del paquete (invertido, único)
package.domain = org.radonapp

# (str) Carpeta con el código fuente donde está main.py
source.dir = .

# (list) Extensiones de archivo a incluir
source.include_exts = py,kv,png,jpg,jpeg,atlas

# (str) Versión de la app
version = 0.1

# (list) Requisitos / dependencias de la app
requirements = python3,kivy==2.3.1,pillow,reportlab,plyer

# (str) Orientación admitida (portrait, landscape o all)
orientation = portrait

# (bool) Indica si la app es de pantalla completa
fullscreen = 0

# (list) Permisos necesarios en Android (cámara para las fotos,
# almacenamiento para adjuntar el plano y guardar el PDF generado)
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) API mínima y objetivo de Android (ajustar según necesidades)
android.minapi = 21
android.api = 34

# (str) Arquitecturas objetivo (arm64-v8a cubre la mayoría de móviles actuales)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Aceptar automáticamente las licencias del SDK de Android
android.accept_sdk_license = True

# (str) Icono de la app (opcional, añadir icon.png de 512x512 si se desea)
# icon.filename = %(source.dir)s/icon.png

[buildozer]

# (int) Nivel de detalle del log (0 = solo error, 1 = info, 2 = debug)
log_level = 2

# (int) Mostrar advertencia si se ejecuta como root
warn_on_root = 1
