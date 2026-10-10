[English](README.md) | [Português](README.pt.md) | [Español](README.es.md)

# DoomTUI

**DoomTUI** is a modern and elegant terminal-based launcher (TUI), developed in Python using the [Textual](https://github.com/Textualize/textual) framework. It was created to easily manage and launch your favorite games based on the Doom engine, organizing IWADs, PWADs (folders and `.wad` or `.pk3` files), and multiple Source Ports in a clean and intuitive way.

<img width="1024" alt="doomtui" src="screenshot.png" />

## 🚀 Features

* **Modern TUI Interface:** Built with Textual, providing keyboard navigation and a clean interface.
* **Automatic Detection:** Scans configured directories to find IWADs and PWADs.
* **Multiple Format Support:** Compatible with `.wad` and `.pk3` files.
* **Loading Modes:** Quickly switch between `-file` (default) and `-merge` (merge) modes.
* **Integrated Configuration Editor:** View or edit the `.ini` configuration file directly from within the application through a modal screen with a built-in text editor.
* **Command Preview:** View the complete command generated in real time, with quick copy support using `xclip` / `wl-clipboard`.

## 🛠️ Requirements

* Python 3.9+
* [pipx](https://pipx.pypa.io/)
* Optional: `xclip` or `wl-clipboard` (copy command to clipboard)

The `textual` library is installed automatically.

## 📦 Installation

1. Install [pipx](https://pipx.pypa.io/stable/installation/) (Debian / Ubuntu / Linux Mint):

```bash
   sudo apt install pipx
   pipx ensurepath
```

   Then restart your terminal.

2. Install DoomTUI:

```bash
   pipx install git+https://github.com/rlins10/doomtui.git
```

   To update later:

```bash
   pipx upgrade doomtui
```

   To uninstall
```
   pipx uninstall doomtui
```

## ⚙️ Configuration

3. DoomTUI automatically creates the configuration file on its first run at:

   ```bash
   ~/.config/doomtui/doomtui.ini
   ```
   * The `doomtui.ini.example` file in the repository is not read by the application; it is only an example.

4. Example of the default **.ini** structure:

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

## 🎮 How to Use

5. Run the main script from the terminal:

   ```bash
   doomtui
   ```
   
   * Use modal edit to configure your engines, iwad and pwad directories
   * Save your .ini
   * Select your options
   * Play

6. Main Keyboard Shortcuts:
   * ctrl-e: Opens the modal editor to modify the doomtui.ini file.
   * ctrl-v: Opens the doomtui.ini file in read-only mode.
   * ctrl-q: Exits the application.
   * Esc: Exits the editor and/or viewer.

## 🗺️ (TODO)

7. Next Steps
   * [ ] Auto-refresh IWAD selections.
   * [ ] Save extra parameters to the `.ini` file.
   * [ ] Add automatic project update checking.
   * [ ] Multi-language support.
   * [ ] Test on Windows.

## 📄 License

   * This project is distributed under the terms of the GNU General Public License v2.0 (GPLv2).
   * See the LICENSE file for more details.
   * Copies are permitted.
