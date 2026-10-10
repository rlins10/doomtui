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

* Python 3.9+
* Bibliotecas de Python:
  * `textual` 8.0 o superior [Repositorio de GitHub](https://github.com/Textualize/textual)

## 📦 Instalación

1. Asegúrate de que tu venv esté configurado correctamente
   * Instrucciones para la creación de entornos virtuales para Python. Visita [Creación de entornos virtuales](https://docs.python.org/es/3/library/venv.html)
   * **No uses** el paquete `textual` de tu distribución (está desactualizado y es incompatible).
   * Para instalar `textual`, sigue las instrucciones del [repositorio de GitHub](https://github.com/Textualize/textual).

2. Clona el repositorio o descarga los fuentes:

   ```bash
   git clone https://github.com/rlins10/doomtui.git
   cd doomtui
   sudo cp doomtui.py /usr/local/bin
   sudo chmod +x /usr/local/bin/doomtui.py
   ```

## ⚙️ Configuración

3. DoomTUI crea automáticamente el archivo de configuración en la primera ejecución en:
    
    ```bash
    ~/.config/doomtui/doomtui.ini
    ```
    * La aplicación no lee el archivo `doomtui.ini.example` del repositorio, es solo un ejemplo.
    
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

   * Este proyecto se distribuye bajo los términos de la licencia GNU General Public License v2.0 (GPLv2). 
   * Consulta el archivo LICENSE para más detalles.
   * Copias permitidas.
