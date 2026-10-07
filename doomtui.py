#!/usr/bin/env python3
#
#   doomtui.py
#  
#   Copyright 2026 Renato Lins <renatolins.am@gmail.com>
#  
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.
#  
#  

import os
import subprocess
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, Static, Select, RadioSet, RadioButton, Input, Button, TextArea, Label
from textual.binding import Binding
from textual.screen import ModalScreen


# editor para o INI    
class IniEditorScreen(ModalScreen):
    """Tela modal com TextArea para visualizar ou editar o arquivo doomtui.ini."""
    
    CSS = """
    ModalScreen {
        align: center middle;
        background: rgba(0, 0, 0, 0.8);
    }
    
    #editor-dialog {
        width: 85%;
        height: 85%;
        border: round $accent;
        border-title-color: $accent;
        border-title-style: bold;
        background: $surface;
        padding: 1;
        layout: vertical;
    }
    
    TextArea {
        height: 1fr;
        border: solid $primary;
        background: $boost;
        margin-bottom: 1;
    }
    
    #modal-buttons {
        layout: horizontal;
        height: auto;
        align: right middle;
    }
    
    #modal-buttons Button {
        margin-left: 2;
    }
    """

    def __init__(self, ini_path: Path, read_only: bool = False):
        super().__init__()
        self.ini_path = ini_path
        self.read_only = read_only

    def compose(self) -> ComposeResult:
        content = ""
        if self.ini_path.exists():
            content = self.ini_path.read_text(encoding="utf-8")
            
        dialog = Container(id="editor-dialog")
        dialog.border_title = "Visualizar doomtui.ini" if self.read_only else "Editar doomtui.ini"
        
        with dialog:
            ta = TextArea(content, show_line_numbers=True, id="ini-textarea")
            if self.read_only:
                ta.read_only = True
            yield ta
            
            with Horizontal(id="modal-buttons"):
                if not self.read_only:
                    yield Button("Salvar e Recarregar", variant="success", id="btn-save-ini")
                yield Button("Fechar", variant="error" if not self.read_only else "default", id="btn-close-ini")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-save-ini":
            textarea = self.query_one("#ini-textarea", TextArea)
            try:
                self.ini_path.write_text(textarea.text, encoding="utf-8")
                self.app.notify("Ficheiro .ini salvo com sucesso!", severity="success")
                if hasattr(self.app, "load_config"):
                    self.app.load_config()
                self.dismiss(True)
            except Exception as e:
                self.app.notify(f"Erro ao salvar: {e}", severity="error")
        elif event.button.id == "btn-close-ini":
            self.dismiss(False)


class DoomLauncherTUI(App):
    """Launcher avançado para WADs de Doom com carregamento via arquivo .ini."""

    BINDINGS = [
        Binding("e", "edit_ini", "Editar INI", priority=True),
        Binding("v", "view_ini", "Ver INI", priority=True),
        Binding("q", "quit", "Sair", priority=True),
    ]

    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }
    
    .boxed-field {
        border: round $accent;
        border-title-color: $accent;
        border-title-style: bold;
        height: 5;
        padding: 0 1;
        margin-bottom: 1;
        align-vertical: middle;
    }

    #iwad-select > SelectCurrent,
    #iwad-select:focus > SelectCurrent,
    #port-select > SelectCurrent,
    #port-select:focus > SelectCurrent {
        border: none;
        background: transparent;
    }

    #extra-input,
    #extra-input:focus {
        border: none;
        background: transparent;
        height: 1;
        padding: 0;
        margin-top: 0;
    }

    #load-mode-set {
        background: transparent;
        height: 3;
        layout: horizontal;
        align-vertical: middle;
    }
    
    #load-mode-set RadioButton {
        background: transparent;
        margin-right: 2;
    }
    
    #top-pane {
        height: 40%;
        layout: horizontal;
        border: solid $primary;
        padding: 1;
        margin: 1;
    }

    #bottom-pane {
        height: 54%;
        border: solid $secondary;
        padding: 1;
        margin: 1;
        layout: vertical;
    }

    .column {
        width: 1fr;
        padding: 0 1;
    }
    
    .dir-header {
        background: $primary;
        color: $text;
        text-style: bold;
        padding: 0 1;
        margin-top: 1;
        margin-bottom: 0;
    }
    
    .pwad-radio {
        margin-left: 2;
        background: transparent;
    }
    
    #pwads-scroll-container {
        height: 1fr;
        border: round $accent;
        border-title-color: $accent;
        border-title-style: bold;
        padding: 1;
        background: $boost;
        margin-top: 0;
        margin-bottom: 1;
    }

    #command-preview {
        background: $panel;
        color: $success;
        padding: 1;
        margin-top: 0;
        margin-bottom: 1;
        border: solid $success;
    }

    #action-buttons {
        layout: horizontal;
        height: auto;
        align: right middle;
    }

    #action-buttons Button {
        margin-left: 2;
    }
    """

    def __init__(self):
        super().__init__()
        
        self.ini_path = Path.home() / ".config" / "doomtui" / "doomtui.ini"
        self.create_default_ini_if_missing()
        
        self.iwad_directories = []
        self.pwad_directories = []
        self.port_options = []
        
        self.selected_port = "gzdoom"
        self.selected_iwad = ""
        self.selected_mode = "-file"
        self.selected_pwad = ""
        self.extra_params = ""
        self.pwad_map = {}
        
        # Apenas lê dados no init (sem tocar na UI) para evitar "No screens on stack"
        self.load_config_data_only()

    def create_default_ini_if_missing(self) -> None:
        """Cria um ficheiro padrão caso o doomtui.ini não exista."""
        
        # Cria o diretório pai (~/.config/doomtui) caso não exista
        self.ini_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.ini_path.exists():
            default_content = """# Este ficheiro foi gerado para o DoomTui https://github.com/rlins10/doomtui.py
[IWADSearch.Directories]
Path=$DOOMWADDIR

[PWAD.Directories]
Path=$HOME/games/doom/doom-pwad
Path=$HOME/games/doom/doom2-pwad
Path=$HOME/games/doom/hexen-pwad
Path=$HOME/games/doom/multi/doom
Path=$HOME/games/doom/multi/doom2

[PORT.Directories]
Port=gzdoom
Port=uzdoom
Port=biaseddoom
Port=$DOOMWADDIR/zandronum/zandronum
"""
            self.ini_path.write_text(default_content, encoding="utf-8")

    def expand_path_smart(self, raw_path: str) -> str:
        """Expande variáveis de ambiente de forma inteligente, garantindo captura do $DOOMWADDIR."""
        if "$DOOMWADDIR" in raw_path and "DOOMWADDIR" not in os.environ:
            try:
                val_env = subprocess.run(
                    ["bash", "-c", "echo $DOOMWADDIR"], 
                    capture_output=True, text=True, check=True
                ).stdout.strip()
                if val_env:
                    os.environ["DOOMWADDIR"] = val_env
            except Exception:
                pass
            
            if "DOOMWADDIR" not in os.environ:
                os.environ["DOOMWADDIR"] = str(Path.home() / "games" / "zdoom")
                
        return os.path.expandvars(raw_path)

    # Substitudo do configparser
    def load_config_data_only(self) -> None:
        """Apenas lê o ficheiro .ini sem tentar manipular widgets da UI."""
        self.iwad_directories = []
        self.pwad_directories = []  # <--- Limpa a lista antes de reler
        raw_ports = []

        if not self.ini_path.exists():
            return

        current_section = None
        
        try:
            with open(self.ini_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith(";"):
                        continue
                    
                    if line.startswith("[") and line.endswith("]"):
                        current_section = line[1:-1].strip()
                        continue
                    
                    if "=" in line and current_section:
                        key, val = line.split("=", 1)
                        key = key.strip().lower()
                        val = val.strip()
                        
                        if not val:
                            continue
                            
                        expanded_val = self.expand_path_smart(val)
                        
                        if current_section.lower() == "iwadsearch.directories" and key == "path":
                            self.iwad_directories.append(Path(expanded_val))
                        elif current_section.lower() == "pwad.directories" and key == "path":
                            self.pwad_directories.append(Path(expanded_val))  # <--- Adiciona corretamente
                        elif current_section.lower() == "port.directories" and key == "port":
                            port_name = Path(expanded_val).stem.capitalize()
                            raw_ports.append((port_name, expanded_val))
                            
        except Exception as e:
            pass

        self.port_options = raw_ports if raw_ports else [("GZDoom", "gzdoom")]

    def load_config(self) -> None:
        """Lê o .ini e atualiza a interface (usado após edição do ficheiro)."""
        self.load_config_data_only()
        try:
            self.refresh_ui_elements()
        except Exception as e:
            self.notify(f"Erro ao atualizar após recarregar: {e}", severity="error")

    def scan_iwads(self):
        """Busca pelos iwads nos diretórios configurados no .ini"""
        iwads = []
        for d in self.iwad_directories:
            if d.exists() and d.is_dir():
                for ext in ("*.wad", "*.WAD"):
                    for file_path in d.glob(ext):
                        iwads.append((file_path.name, str(file_path)))
        iwads.sort(key=lambda item: item[0].lower())
        seen = set()
        unique_iwads = []
        for name, path in iwads:
            if path not in seen:
                seen.add(path)
                unique_iwads.append((name, path))
        return unique_iwads

    def scan_pwads(self) -> list:
        """Varre os diretórios configurados e retorna uma lista estruturada de pastas e ficheiros de PWAD."""
        structured_pwads = []
        for d in self.pwad_directories:
            if not d.exists() or not d.is_dir():
                continue
                
            files_in_dir = []
            for ext in ("*.wad", "*.WAD", "*.pk3", "*.PK3"):
                files_in_dir.extend(d.glob(ext))
            
            if files_in_dir:
                try:
                    folder_label = str(d.relative_to(Path.home()))
                except ValueError:
                    folder_label = d.name
                    
                file_items = sorted([f.name for f in files_in_dir], key=lambda x: x.lower())
                file_paths = {f.name: str(f) for f in files_in_dir}
                
                structured_pwads.append({
                    "folder": folder_label,
                    "files": file_items,
                    "paths": file_paths
                })
        return structured_pwads

    #
    def populate_pwads_container(self) -> None:
        """Gera e reconstrói os grupos de PWADs de forma segura e limpa."""
        sc = self.query_one("#pwads-scroll-container", ScrollableContainer)
        sc.remove_children()
        
        pwad_data = self.scan_pwads()
        self.pwad_map = {}
        global_index = 0
        
        widgets_to_mount = []
        
        for group in pwad_data:
            # Adiciona o título da pasta como um Static separado
            widgets_to_mount.append(Static(f"📂 {group['folder']}", classes="dir-header"))
            
            # Cria os RadioButtons para os ficheiros desta pasta específica
            radio_buttons = []
            for filename in group["files"]:
                safe_id = f"pwad_{global_index}"
                full_path = group["paths"][filename]
                self.pwad_map[safe_id] = full_path
                radio_buttons.append(RadioButton(filename, id=safe_id, classes="pwad-radio"))
                global_index += 1
            
            # Cada pasta ganha o seu RadioSet próprio apenas com RadioButtons
            if radio_buttons:
                widgets_to_mount.append(RadioSet(*radio_buttons))

        if widgets_to_mount:
            for w in widgets_to_mount:
                sc.mount(w)
        else:
            sc.mount(Static("Nenhum PWAD encontrado nas pastas do .ini", classes="dir-header"))
    
    #
    def refresh_ui_elements(self) -> None:
        """Atualiza toda a interface após recarregar o .ini."""
        try:
            # 1. Atualiza IWADs
            iwad_select = self.query_one("#iwad-select", Select)
            iwad_options = self.scan_iwads()
            if not iwad_options:
                iwad_options = [("Nenhum IWAD encontrado", "")]
            iwad_select.set_options(iwad_options)
            
            # Seleciona o primeiro IWAD automaticamente se houver opções válidas
            if iwad_options and iwad_options[0][1]:
                iwad_select.value = iwad_options[0][1]
                self.selected_iwad = iwad_options[0][1]
            else:
                iwad_select.value = Select.BLANK
                self.selected_iwad = ""

            # 2. Atualiza Ports
            port_select = self.query_one("#port-select", Select)
            port_select.set_options(self.port_options)
            if self.port_options:
                self.selected_port = self.port_options[0][1]
                port_select.value = self.selected_port

            # 3. Reconstrói os PWADs usando o método seguro
            self.populate_pwads_container()
            
            # Actualiza o preview do comando com os valores correntes
            self.update_command_preview()
            
            self.notify("Configurações do .ini recarregadas com sucesso!", severity="information")
        except Exception as e:
            self.notify(f"Erro ao atualizar UI: {e}", severity="error")

    def on_mount(self) -> None:
        """Executado quando a aplicação já está montada e pronta na tela."""
        if self.port_options:
            self.selected_port = self.port_options[0][1]
        self.update_command_preview()

    def compose(self) -> ComposeResult:
        """Constrói a janela principal"""
        yield Header(show_clock=True)
        
        with Container(id="top-pane"):
            with Vertical(classes="column"):
                iwad_options = self.scan_iwads()
                if not iwad_options:
                    iwad_options = [("Nenhum IWAD encontrado", "")]
                
                sel_iwad = Select(iwad_options, prompt="Escolha o IWAD", id="iwad-select", classes="boxed-field")
                sel_iwad.border_title = "1. Selecione o IWAD"
                yield sel_iwad
                
                with Container(classes="boxed-field", id="mode-container") as c_mode:
                    c_mode.border_title = "2. Modo de Carregamento"
                    with RadioSet(id="load-mode-set"):
                        yield RadioButton("-file (Padrão)", value=True, id="mode-file")
                        yield RadioButton("-merge (Mesclagem)", id="mode-merge")

            with Vertical(classes="column"):
                sel_port = Select(self.port_options, value=self.port_options[0][1] if self.port_options else "gzdoom", id="port-select", classes="boxed-field")
                sel_port.border_title = "3. Selecione o Port"
                yield sel_port

                with Container(classes="boxed-field", id="input-container") as c_input:
                    c_input.border_title = "4. Parâmetros Extras"
                    yield Input(placeholder="Ex: -nosound -window", id="extra-input")

        with Container(id="bottom-pane"):
            sc = ScrollableContainer(id="pwads-scroll-container")
            sc.border_title = "5. Selecione o PWAD"
            with sc: 
                pwad_data = self.scan_pwads()
                self.pwad_map = {}
                global_index = 0
                with RadioSet(id="pwads-radioset"):
                    for group in pwad_data:
                        yield Static(f"📂 {group['folder']}", classes="dir-header")
                        for filename in group["files"]:
                            safe_id = f"pwad_{global_index}"
                            full_path = group["paths"][filename]
                            self.pwad_map[safe_id] = full_path
                            yield RadioButton(filename, id=safe_id, classes="pwad-radio")
                            global_index += 1
            
            yield Static("Comando: (configure as opções)", id="command-preview")

            with Horizontal(id="action-buttons"):
                yield Button("Copiar Comando", variant="default", id="btn-copy")
                yield Button("Executar", variant="success", id="btn-run")
                yield Button("Sair", variant="error", id="btn-quit")

        yield Footer()

    def action_edit_ini(self) -> None:
        self.push_screen(IniEditorScreen(self.ini_path, read_only=False))

    def action_view_ini(self) -> None:
        self.push_screen(IniEditorScreen(self.ini_path, read_only=True))

    def build_command_string(self) -> str:
        extra_part = self.extra_params.strip()
        
        if "slade" in self.selected_port.lower():
            paths = []
            if self.selected_iwad:
                paths.append(f'"{self.selected_iwad}"')
            if self.selected_pwad:
                paths.append(f'"{self.selected_pwad}"')
            
            parts = [self.selected_port] + paths
            if extra_part:
                parts.append(extra_part)
            return " ".join(parts)
            
        iwad_path = self.selected_iwad if self.selected_iwad else ""
        iwad_part = f'-iwad "{iwad_path}"' if iwad_path else '-iwad ""'
        pwad_part = f'{self.selected_mode} "{self.selected_pwad}"' if self.selected_pwad else ''
        
        parts = [self.selected_port, iwad_part, pwad_part, extra_part]
        return " ".join([p for p in parts if p])

    def update_command_preview(self) -> None:
        try:
            preview = self.query_one("#command-preview", Static)
            cmd = self.build_command_string()
            preview.update(f"Comando: {cmd}")
        except Exception:
            pass

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "iwad-select":
            self.selected_iwad = event.value if event.value is not Select.BLANK else ""
        elif event.select.id == "port-select":
            if event.value is not Select.BLANK:
                self.selected_port = str(event.value)
        
        self.update_command_preview()


    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        radio_id = event.pressed.id
        if not radio_id:
            return
            
        if radio_id in ("mode-file", "mode-merge"):
            self.selected_mode = "-file" if radio_id == "mode-file" else "-merge"
        elif radio_id.startswith("pwad_"):
            self.selected_pwad = self.pwad_map.get(radio_id, "")
            
        self.update_command_preview()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "extra-input":
            self.extra_params = event.value
            self.update_command_preview()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        cmd = self.build_command_string()
        
        if button_id == "btn-quit":
            self.exit()
        elif button_id == "btn-copy":
            try:
                subprocess.run(["xclip", "-selection", "clipboard"], input=cmd.encode("utf-8"), check=True)
                self.notify("Comando copiado para a área de transferência!")
            except (subprocess.SubprocessError, FileNotFoundError):
                try:
                    subprocess.run(["wl-copy"], input=cmd.encode("utf-8"), check=True)
                    self.notify("Comando copiado (Wayland)!")
                except Exception:
                    self.notify("Erro: Instale xclip ou wl-clipboard para copiar.", severity="error")
        elif button_id == "btn-run":
            if not self.selected_iwad:
                self.notify("Selecione um IWAD antes de executar!", severity="warning")
                return
            try:
                subprocess.Popen(cmd, shell=True)
                self.exit()
            except Exception as e:
                self.notify(f"Erro ao iniciar o jogo: {e}", severity="error")


if __name__ == "__main__":
    app = DoomLauncherTUI()
    app.run()
