[English](README.md) | [Português](README.pt.md) | [Español](README.es.md)

# DoomTUI

**DoomTUI** é um launcher moderno e elegante baseado em terminal (TUI), desenvolvido em Python utilizando o framework [Textual](https://github.com/Textualize/textual). Ele foi criado para gerenciar e iniciar facilmente os seus jogos favoritos baseados na engine Doom, organizando IWADs, PWADs (pastas e arquivos `.wad` ou `.pk3`) e múltiplos Source Ports de forma limpa e intuitiva.


<img width="1024"  alt="doomtui" src="screenshot.png" />

## 🚀 Funcionalidades

* **Interface TUI Moderna:** Construída com Textual, oferecendo navegação por teclado e visual limpo.
* **Detecção Automática:** Varredura de diretórios configurados para encontrar IWADs e PWADs.
* **Suporte a Múltiplos Formatos:** Compatível com arquivos `.wad` e `.pk3`.
* **Modos de Carregamento:** Alternância rápida entre `-file` (padrão) e `-merge` (mesclagem).
* **Editor de Configuração Integrado:** Visualize ou edite o arquivo de configuração `.ini` diretamente de dentro da aplicação através de uma tela modal com editor de texto embutido.
* **Pré-visualização de Comandos:** Acompanhe o comando completo gerado em tempo real, com suporte a cópia rápida para a área de transferência (`xclip` / `wl-clipboard`).

## 🛠️ Requisitos

* Python 3.9+ ou superior
* Bibliotecas Python:
  * `textual` [Repositório do Github](https://github.com/Textualize/textual)

## 📦 Instalação

1. Clone o repositório ou baixe os fontes:

   ```bash
   pip install textual
   git clone https://github.com/rlins10/doomtui.git
   cd doomtui
   sudo cp doomtui.py /usr/local/bin
   sudo chmod +x /usr/local/bin/doomtui.py
   ```

## ⚙️  Configuração

2. O DoomTUI cria automaticamente o arquivo de configuração na primeira execução em:
    
    ```bash
    ~/.config/doomtui/doomtui.ini
    ```

3. Exemplo da estrutura padrão do **.ini:**

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
    
## 🎮 Como Usar

4. Execute o script principal a partir do terminal:

   ```bash
   doomtui.py
   ```
   * Use o Editor para configurar os diretórios dos seus ports, iwad, e pwad
   * Salve seu .ini
   * Selecione suas opções
   * Jogue a vontade

5. Atalhos de Teclado Principais:
   * ctrl-e: Abre o editor modal para alterar o arquivo doomtui.ini.
   * ctrl-v: Abre o modo somente leitura do ficheiro doomtui.ini.
   * ctrl-q: Sai da aplicação.
   * Esc: sair do editor e/ou visualizador

## 🗺️ (TODO)

6. Próximos Passos
   * [ ] Auto Refresh das seleções do iwad.
   * [ ] Salvar os parametros extras no .ini.
   * [ ] Adicionar checagem automática de atualizações do projeto.
   * [ ] Multi-linguagem
   * [ ] Testar no windows

## 📄 Licença

   Este projeto é distribuído sob os termos da licença GNU General Public License v2.0 (GPLv2). 
   Consulte o ficheiro LICENSE para mais detalhes.
   
   Cópias Permitidas.


