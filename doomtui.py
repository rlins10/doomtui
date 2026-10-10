#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import os
import shlex
import subprocess
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import (
    Header, Footer, Static, Select, RadioSet, RadioButton,
    Input, Button, TextArea
)
from textual import on
from textual.widgets import OptionList
from textual.widgets.option_list import Option

# FIX-ME: Remover o loggin quando terminar as depurações
import logging

logging.basicConfig(
    filename="/tmp/doomtui-debug.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Globais
__version__ = "0.8.5"
PWAD_NONE_ID = "pwad_none"

class IniEditorScreen(ModalScreen):
    """Tela modal para visualizar ou editar o arquivo doomtui.ini."""

    BINDINGS = [Binding("escape", "close", "Fechar")]

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

    def action_close(self) -> None:
        self.dismiss(False)

    def compose(self) -> ComposeResult:
        content = ""

        if self.ini_path.exists():
            content = self.ini_path.read_text(encoding="utf-8")

        dialog = Container(id="editor-dialog")
        dialog.border_title = "Visualizar doomtui.ini" if self.read_only else "Editar doomtui.ini"

        with dialog:
            textarea = TextArea(content, show_line_numbers=True, id="ini-textarea")
            textarea.read_only = self.read_only
            yield textarea

            with Horizontal(id="modal-buttons"):
                if not self.read_only:
                    yield Button("Salvar e Recarregar", variant="success", id="btn-save-ini")
                yield Button("Fechar", variant="error" if not self.read_only else "default", id="btn-close-ini")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-save-ini":
            textarea = self.query_one("#ini-textarea", TextArea)

            try:
                self.ini_path.write_text(textarea.text, encoding="utf-8")
                self.app.notify("Arquivo .ini salvo com sucesso!")
                self.app.load_config()
                self.dismiss(True)
            except Exception as e:
                self.app.notify(f"Erro ao salvar: {e}", severity="error")

        elif event.button.id == "btn-close-ini":
            self.dismiss(False)


class DoomLauncherTUI(App):
    """Launcher para WADs de Doom com configuração através de arquivo .ini."""

    BINDINGS = [
        Binding("ctrl+e", "edit_ini", "Editar INI"),
        Binding("ctrl+v", "view_ini", "Ver INI"),
        Binding("ctrl+q", "quit", "Sair"),
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
    
    #pwad-list {
         width: 100%;
         height: 1fr;
         border: round $accent;
         border-title-color: $accent;
         border-title-style: bold;
    }

    #pwad-list > .option-list--option-disabled {
        color: $accent;
        text-style: bold;
    }
    """

    default_ini_content = """# Este arquivo foi gerado para o DoomTui
# https://github.com/rlins10/doomtui

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

    def __init__(self):
        super().__init__()

        # O HOME é usado somente para localizar o próprio arquivo .ini.
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

        # Lê somente os dados. A interface ainda não existe neste ponto.
        self.load_config_data_only()

    def create_default_ini_if_missing(self) -> None:
        """Cria um .ini padrão caso ele ainda não exista."""

        self.ini_path.parent.mkdir(parents=True, exist_ok=True)
        if self.ini_path.exists():
            return
        self.ini_path.write_text(self.default_ini_content, encoding="utf-8")

    def expand_path_smart(self, raw_path: str) -> str:
        """Expande variáveis de ambiente presentes no caminho."""
        return os.path.expandvars(raw_path)

    def load_config_data_only(self) -> None:
        """Lê o .ini sem manipular widgets da interface."""

        self.iwad_directories = []
        self.pwad_directories = []
        raw_ports = []
        if not self.ini_path.exists():
            return
        current_section = None

        try:
            with open(self.ini_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith("#") or line.startswith(";"):
                        continue

                    if line.startswith("[") and line.endswith("]"):
                        current_section = line[1:-1].strip().lower()
                        continue

                    if "=" not in line or not current_section:
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip().lower()
                    value = value.strip()

                    if not value:
                        continue

                    if current_section == "iwadsearch.directories" and key == "path":
                        self.iwad_directories.append({
                            "raw": value,
                            "path": Path(self.expand_path_smart(value))
                        })

                    elif current_section == "pwad.directories" and key == "path":
                        self.pwad_directories.append({
                            "raw": value,
                            "path": Path(self.expand_path_smart(value))
                        })

                    elif current_section == "port.directories" and key == "port":
                        expanded = self.expand_path_smart(value)
                        port_name = Path(expanded).name.capitalize()
                        raw_ports.append((port_name, expanded))

        except Exception:
            logging.exception("Erro ao ler %s", self.ini_path)
            self.port_options = [("GZDoom", "gzdoom")]
            return

        self.port_options = raw_ports if raw_ports else [("GZDoom", "gzdoom")]

    def load_config(self) -> None:
        """Relê o .ini e atualiza a interface."""

        old_iwad = self.selected_iwad
        self.load_config_data_only()
        try:
            self.refresh_ui_elements(old_iwad)
        except Exception as e:
            self.notify(f"Erro ao atualizar após recarregar: {e}", severity="error")

    def scan_iwads(self) -> list:
        """Procura IWADs somente nos diretórios configurados no .ini."""

        iwads = []

        for directory_info in self.iwad_directories:
            directory = directory_info["path"]

            if not directory.exists() or not directory.is_dir():
                logging.debug("Pasta ignorada (não existe): %s", directory)
                continue

            try:
                for file_path in directory.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() == ".wad":
                        iwads.append((file_path.name, str(file_path)))
            except OSError:
                logging.warning("Sem acesso a pasta (iwads): %s", directory)
                continue

        iwads.sort(key=lambda item: item[0].lower())
        seen = set()
        unique_iwads = []

        for name, path in iwads:
            if path not in seen:
                seen.add(path)
                unique_iwads.append((name, path))

        return unique_iwads

    def scan_pwads(self) -> list:
        """Procura PWADs somente nos diretórios configurados no .ini."""

        structured_pwads = []
        # busca por arquivos.
        for directory_info in self.pwad_directories:
            directory = directory_info["path"]
            if not directory.exists() or not directory.is_dir():
                logging.warning("Pasta ignorada (não exite) (pwads): %s", directory)
                continue
            files_in_dir = []
            try:
                for file_path in directory.iterdir():
                    if not file_path.is_file():
                        continue
                    if file_path.suffix.lower() in (".wad", ".pk3"):
                        files_in_dir.append(file_path)
            except OSError:
                logging.warning("Sem acesso a pasta  (pwads): %s", directory)
                continue

            if not files_in_dir:
                continue

            files_in_dir.sort(key=lambda item: item.name.lower())
            file_items = [file_path.name for file_path in files_in_dir]
            file_paths = {file_path.name: str(file_path) for file_path in files_in_dir}
            structured_pwads.append({
                "folder": str(directory),
                "files": file_items,
                "paths": file_paths
            })

        return structured_pwads

    #
    def populate_pwad_list(self) -> None:
        """Reconstrói o OptionList de PWADs a partir do .ini."""

        pwad_list = self.query_one("#pwad-list", OptionList)
        pwad_list.clear_options()
        self.pwad_map = {}
        global_index = 0

        # Opção fixa: remove o PWAD do comando final
        pwad_list.add_option(Option("✖ Nenhum PWAD", id=PWAD_NONE_ID))

        for group in self.scan_pwads():
            pwad_list.add_option(None)  # separador
            # Cabeçalho do diretório (não selecionável)
            pwad_list.add_option(Option(f"📂 {group['folder']}", disabled=True))

            for filename in group["files"]:
                safe_id = f"pwad_{global_index}"
                self.pwad_map[safe_id] = group["paths"][filename]
                pwad_list.add_option(Option(f"  {filename}", id=safe_id))
                global_index += 1

        if not self.pwad_map:
            pwad_list.add_option(None)
            pwad_list.add_option(Option("Nenhum PWAD encontrado nas pastas do .ini", disabled=True))

        # O PWAD anterior pode não existir mais após recarregar.
        if self.selected_pwad not in self.pwad_map.values():
            self.selected_pwad = ""

    def refresh_ui_elements(self, old_iwad: str = "") -> None:
        """Atualiza a interface depois de recarregar o .ini."""

        # IWAD
        iwad_select = self.query_one("#iwad-select", Select)
        iwad_options = self.scan_iwads()
        if not iwad_options:
            iwad_select.set_options([("Nenhum IWAD encontrado", "")])
            self.selected_iwad = ""
        else:
            iwad_select.set_options(iwad_options)
            valid_paths = [path for _, path in iwad_options]
            if old_iwad in valid_paths:
                self.selected_iwad = old_iwad
            else:
                self.selected_iwad = iwad_options[0][1]

            iwad_select.value = self.selected_iwad

        # Port
        port_select = self.query_one("#port-select", Select)
        port_select.set_options(self.port_options)
        if self.port_options:
            valid_ports = [value for _, value in self.port_options]
            if self.selected_port not in valid_ports:
                self.selected_port = self.port_options[0][1]

            port_select.value = self.selected_port

        # PWADs
        self.populate_pwad_list()
        self.update_command_preview()
        self.notify("Configurações do .ini recarregadas com sucesso!", severity="information")

    def on_mount(self) -> None:
        """Executado quando a interface já está montada."""

        self.populate_pwad_list()
        iwad_options = self.scan_iwads()
        if iwad_options:
            self.selected_iwad = iwad_options[0][1]
            try:
                self.query_one("#iwad-select", Select).value = self.selected_iwad
            except Exception:
                pass

        if self.port_options:
            self.selected_port = self.port_options[0][1]

        self.update_command_preview()

    # compose
    def compose(self) -> ComposeResult:
        """Constrói a interface principal."""

        yield Header(show_clock=True)
        # conteiner de cima
        with Container(id="top-pane"):
            with Vertical(classes="column"):
                iwad_options = self.scan_iwads()

                if not iwad_options:
                    iwad_options = [("Nenhum IWAD encontrado", "")]

                select_iwad = Select(iwad_options,
                    allow_blank=False,id="iwad-select",classes="boxed-field")
                select_iwad.border_title = "1. Selecione o IWAD"
                yield select_iwad

                with Container(classes="boxed-field",id="mode-container") as mode_container:
                    mode_container.border_title = "2. Modo de Carregamento"

                    with RadioSet(id="load-mode-set"):
                        yield RadioButton("-file (Padrão)",value=True,id="mode-file")
                        yield RadioButton("-merge (Mesclagem)",id="mode-merge")

            # Select dos source ports
            with Vertical(classes="column"):
                select_port = Select(
                    self.port_options,
                    value=(self.port_options[0][1] if self.port_options else "gzdoom"),
                    allow_blank=False,id="port-select",classes="boxed-field"
                )
                select_port.border_title = "3. Selecione o Port"
                yield select_port

                with Container(classes="boxed-field",id="input-container") as input_container:
                    input_container.border_title = "4. Parâmetros Extras"
                    yield Input(placeholder="Ex: -nosound -window",id="extra-input")
                    
        #conteiner de baixo
        with Container(id="bottom-pane"):
            pwad_list = OptionList(id="pwad-list")
            pwad_list.border_title = "5. Selecione o PWAD"
            yield pwad_list # preenchido no on_mount
            yield Static("Comando: ",id="command-preview")

            with Horizontal(id="action-buttons"):
                btn_copy = Button("Copiar Comando", variant="default", id="btn-copy")
                btn_copy.tooltip = "Copia o comando para rodar no terminal e ver os logs do jogo"
                yield btn_copy
                yield Button("Executar",variant="success",id="btn-run")
                yield Button("Sair",variant="error",id="btn-quit")

        yield Footer()

    ###
    def action_edit_ini(self) -> None:
        if isinstance(self.screen, IniEditorScreen):
            return
        self.push_screen(IniEditorScreen(self.ini_path, read_only=False))

    def action_view_ini(self) -> None:
        if isinstance(self.screen, IniEditorScreen):
            return
        self.push_screen(IniEditorScreen(self.ini_path, read_only=True))

    def build_command_args(self) -> list[str]:
        """Monta os argumentos reais do comando.
        Lança ValueError se os parâmetros extras tiverem aspas não fechadas.
        """

        if not self.selected_port:
            return []

        args = [self.selected_port]
        if "slade" in self.selected_port.lower():
            if self.selected_iwad:
                args.append(self.selected_iwad)

            if self.selected_pwad:
                args.append(self.selected_pwad)
        else:
            args.extend(["-iwad", self.selected_iwad])

            if self.selected_pwad:
                args.extend([self.selected_mode, self.selected_pwad])

        extra = self.extra_params.strip()
        if extra:
            args.extend(shlex.split(extra))  # pode lançar ValueError

        return args

    def build_command_string(self) -> str:
        """Versão legível do comando, com quoting seguro para o shell.
        Lança ValueError se os parâmetros extras tiverem aspas não fechadas.
        """
        return shlex.join(self.build_command_args())


    # Atualiza a linha de comando
    def update_command_preview(self) -> None:
        try:
            preview = self.query_one("#command-preview", Static)
            try:
                text = f"Comando: {self.build_command_string()}"
            except ValueError:
                text = "Comando: ⚠ aspas não fechadas nos parâmetros extras"

            preview.update(text)
            pwad_list = self.query_one("#pwad-list", OptionList)
            pwad_list.border_subtitle = (
                Path(self.selected_pwad).name if self.selected_pwad else "nenhum"
            )
        except Exception:
            pass

    # handler do pwad Option List
    @on(OptionList.OptionSelected, "#pwad-list")
    def on_pwad_selected(self, event: OptionList.OptionSelected) -> None:
        """Atualiza o PWAD selecionado e o preview do comando."""

        if event.option_id is None:
            return

        if event.option_id == PWAD_NONE_ID:
            self.selected_pwad = ""
            self.update_command_preview()
            return

        pwad_path = self.pwad_map.get(event.option_id)
        if pwad_path is None:
            return

        self.selected_pwad = pwad_path
        self.update_command_preview()
        
    @on(Select.Changed, "#iwad-select")
    def on_iwad_changed(self, event):
        """Atualiza o iwad selecionado e o preview do comando."""
        self.selected_iwad = event.value
        self.update_command_preview()

    # handler do Select de Port
    @on(Select.Changed, "#port-select")
    def on_port_changed(self, event: Select.Changed) -> None:
        """Atualiza o port selecionado e o preview do comando."""
        self.selected_port = event.value
        self.update_command_preview()

    # handler do -file e -merge
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        radio_id = event.pressed.id
        if not radio_id:
            return
        if radio_id == "mode-file":
            self.selected_mode = "-file"
        elif radio_id == "mode-merge":
            self.selected_mode = "-merge"
        self.update_command_preview()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "extra-input":
            self.extra_params = event.value
            self.update_command_preview()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn-quit":
            self.exit()
            return
        if button_id == "btn-copy":
            try:
                command = self.build_command_string()
            except ValueError:
                self.notify("Parâmetros extras com aspas não fechadas.",severity="warning")
                return

            for clip_cmd in (["xclip", "-selection", "clipboard"], ["wl-copy"]):
                try:
                    subprocess.run(
                        clip_cmd,
                        input=command.encode("utf-8"),
                        check=True
                    )
                    self.notify("Comando copiado para a área de transferência!")
                    return
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue

            self.notify("Erro: instale xclip ou wl-clipboard para copiar.",severity="error")
            return
            
        if button_id == "btn-run":
            if not self.selected_iwad:
                self.notify("Selecione um IWAD antes de executar!",severity="warning")
                return

            try:
                args = self.build_command_args()
            except ValueError:
                self.notify(
                    "Parâmetros extras com aspas não fechadas.",
                    severity="warning"
                )
                return

            if not args:
                self.notify("Nenhum Port foi configurado.",severity="error")
                return

            try:
                logging.info("Executando: %s", shlex.join(args))
                subprocess.Popen(
                    args,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
                self.exit()

            except FileNotFoundError:
                self.notify(f"Port não encontrado: {self.selected_port}",severity="error")

            except OSError as e:
                self.notify(f"Erro ao iniciar o jogo: {e}",severity="error")
##
## Main 
##
if __name__ == "__main__":
    app = DoomLauncherTUI()
    app.run()
