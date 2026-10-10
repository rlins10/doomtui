[English](README.md) | [Português](README.pt.md) | [Español](README.es.md)

# DoomTUI

**DoomTUI** es un lanzador moderno y elegante basado en terminal (TUI), desarrollado en Python utilizando el framework [Textual](https://github.com/Textualize/textual). Fue creado para gestionar e iniciar fácilmente tus juegos favoritos basados en el motor Doom, organizando IWADs, PWADs (carpetas y archivos `.wad` o `.pk3`) y múltiples Source Ports de forma limpia e intuitiva.

<img width="1024"  alt="doomtui" src="screenshot.png" />

## 🚀 Funcionalidades

* **Interfaz TUI Moderna:** Construida con Textual, ofreciendo navegación por teclado y una apariencia limpia.
* **Detección Automática:** Escaneo de directorios configurados para encontrar IWADs y PWADs.
* **Soporte para Múltiples Formatos:** Compatible con archivos `.wad` y `.pk3`.
* **Modos de Carga:** Alternancia rápida entre `-file` (predeterminado) y `-merge` (fusión).
* **Editor de Configuración Integrado:** Visualiza o edita el archivo de configuración `.ini` directamente desde la aplicación a través de una pantalla modal con un editor de texto integrado.
* **Vista previa de Comandos:** Sigue el comando completo generado en tiempo real, con soporte para copia rápida al portapapeles (`xclip` / `wl-clipboard`).

## 🛠️ Requisitos

* Python 3.9 o superior
* Bibliotecas de Python:
  * `textual` 8.0 o superior [Repositorio de Github](https://github.com/Textualize/textual)

## 📦 Instalación

1. Clona el repositorio o descarga los fuentes:

   ```bash
   pip install textual
   git clone https://github.com/rlins10/doomtui.git
   cd doomtui
   sudo cp doomtui.py /usr/local/bin
   sudo chmod +x /usr/local/bin/doomtui.py
   ```

2. Para la instalación de `textual` sin pip, visita el [Repositorio de Github](https://github.com/Textualize/textual)

## ⚙️ Configuración

3. DoomTUI crea automáticamente el archivo de configuración en la primera ejecución en:
    
    ```bash
    ~/.config/doomtui/doomtui.ini
    ```

4. Ejemplo de la estructura predeterminada del **.ini:**

    ```ini
    [IWADSearch.Directories]
    Path=$DOOMWADDIR
    Path=$HOME/games/others

    [PWAD.Directories]
    Path=$HOME/games/doom/doom-pwad
    Path=$HOME/games/doom/doom2-pwad

    [PORT.Directories]
    Port=gzdoom
    Port=uzdoom
    Port=$HOME/games/zandronum/zandronum
    ```
    
## 🎮 Cómo Usar

5. Ejecuta el script principal desde la terminal:

   ```bash
   doomtui.py
   ```
   * Usa el editor para configurar los directorios de tus ports, iwads y pwads
   * Guarda tu archivo .ini
   * Selecciona tus opciones
   * Juega a gusto

6. Atajos de Teclado Principales:
   * ctrl-e: Abre el editor modal para modificar el archivo doomtui.ini.
   * ctrl-v: Abre el modo de solo lectura del archivo doomtui.ini.
   * ctrl-q: Sale de la aplicación.
   * Esc: Sale del editor y/o visor.

## 🗺️ (TODO)

7. Próximos Pasos
   * [ ] Actualización automática (Auto Refresh) de las selecciones de iwad.
   * [ ] Guardar los parámetros adicionales en el .ini.
   * [ ] Añadir comprobación automática de actualizaciones del proyecto.
   * [ ] Soporte multiidioma.
   * [ ] Probar en Windows.

## 📄 Licencia

   Este proyecto se distribuye bajo los términos de la licencia GNU General Public License v2.0 (GPLv2). 
   Consulta el archivo LICENSE para más detalles.
   
   Copias permitidas.
