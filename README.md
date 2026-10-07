# DoomTUI

**DoomTUI** é um launcher moderno e elegante baseado em terminal (TUI), desenvolvido em Python utilizando o framework [Textual](https://github.com/Textualize/textual). Ele foi criado para gerenciar e iniciar facilmente os seus jogos favoritos baseados na engine Doom, organizando IWADs, PWADs (pastas e arquivos `.wad` ou `.pk3`) e múltiplos Source Ports de forma limpa e intuitiva.


<img width="1277" height="1024" alt="doomtui" src="https://github.com/user-attachments/assets/84b9dc79-c627-4e9c-9a97-bbbda277d328" />


---

## 🚀 Funcionalidades

* **Interface TUI Moderna:** Construída com Textual, oferecendo navegação por teclado e visual limpo.
* **Detecção Automática:** Varredura de diretórios configurados para encontrar IWADs e PWADs.
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

   ```bash
   git clone [https://github.com/rlins10/doomtui.git](https://github.com/rlins10/doomtui.git)
   cd doomtui
   cp doomtui.py /usr/local/bin
   chmod +x /usr/local/bin/doomtui.py

## ⚙️  Configuração

2. O DoomTUI cria automaticamente o arquivo de configuração na primeira execução em:
    
    ```bash
    ~/.config/doomtui/doomtui.ini

3. Exemplo da estrutura padrão do **.ini:**

    ```bash
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

4. Execute o script principal a partir do terminal:

   ```
   doomtiu.py

5. Atalhos de Teclado Principais:
   e: Abre o editor modal para alterar o ficheiro doomtui.ini.
   v: Abre o modo somente leitura do ficheiro doomtui.ini.
   q: Sai da aplicação.

## 🗺️ (TODO)

6. Próximos Passos
* [ ] Auto Refresh das seleções do iwad.
* [ ] Salvar os parametros extras no .ini.
* [ ] Adicionar checagem automática de atualizações do projeto.

## 📄 Licença
   Este projeto é distribuído sob os termos da licença GNU General Public License v2.0 (GPLv2). 
   Consulte o ficheiro LICENSE para mais detalhes.
   Copias Permitidas.
