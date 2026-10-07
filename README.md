# DoomTUI

**DoomTUI** é um launcher moderno e elegante baseado em terminal (TUI), desenvolvido em Python utilizando o framework [Textual](https://github.com/Textualize/textual). Ele foi criado para gerenciar e iniciar facilmente os seus jogos favoritos baseados na engine Doom, organizando IWADs, PWADs (pastas e arquivos `.wad` ou `.pk3`) e múltiplos Source Ports de forma limpa e intuitiva.

---

## 🚀 Funcionalidades

* **Interface TUI Moderna:** Construída com Textual, oferecendo navegação por teclado e visual limpo.
* **Detecção Automática:** Varredura recursiva de diretórios configurados para encontrar IWADs e PWADs.
* **Suporte a Múltiplos Formatos:** Compatível com arquivos `.wad` e `.pk3`.
* **Modos de Carregamento:** Alternância rápida entre `-file` (padrão) e `-merge` (mesclagem).
* **Editor de Configuração Integrado:** Visualize ou edite o arquivo de configuração `.ini` diretamente de dentro da aplicação através de uma tela modal com editor de texto embutido.
* **Pré-visualização de Comandos:** Acompanhe o comando completo gerado em tempo real, com suporte a cópia rápida para a área de transferência (`xclip` / `wl-clipboard`).

---

## 🛠️ Requisitos

* Python 3.8 ou superior
* Bibliotecas Python:
  * `textual`

---

## 📦 Instalação

1. Clone o repositório ou baixe os fontes:

   git clone [https://github.com/rlins10/doomtui.py.git](https://github.com/rlins10/doomtui.py.git)
   cd doomtui.py
   cp doomtui.py /usr/local/bin
   chmod +x /usr/local/bin/doomtui.py

## ⚙️  Configuração

    O DoomTUI cria automaticamente o arquivo de configuração na primeira execução em:

    ~/.config/doomtui/doomtui.ini

    Exemplo da estrutura padrão do **.ini:**

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

## 🎮 Como Usar

1. Execute o script principal a partir do terminal:

   doomtiu.py

2. Atalhos de Teclado Principais:
   e: Abre o editor modal para alterar o ficheiro doomtui.ini.
   v: Abre o modo somente leitura do ficheiro doomtui.ini.
   q: Sai da aplicação.

## 📄 Licença
   Este projeto é distribuído sob os termos da licença GNU General Public License v2.0 (GPLv2). 
   Consulte o ficheiro LICENSE para mais detalhes.
   Copias Permitidas.
