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

* Python 3.9+
* Bibliotecas Python:
  * `textual` 8.0 ou maior [Repositório do GitHub](https://github.com/Textualize/textual)

## 📦 Instalação

1. Certifique-se de que o seu venv está configurado corretamente
   * Instruções de criação de ambientes virtuais para o Python. Visite [Criação de ambientes virtuais](https://docs.python.org/pt-br/3/library/venv.html)
   * **Não use** o pacote `textual` da sua distribuição (versão antiga e incompatível).
   * Para instalar o `textual`, siga as instruções do [repositório do GitHub](https://github.com/Textualize/textual).

2. Clone o repositório ou baixe os fontes:

   ```bash
   git clone https://github.com/rlins10/doomtui.git
   cd doomtui
   sudo cp doomtui.py /usr/local/bin
   sudo chmod +x /usr/local/bin/doomtui.py
   ```

## ⚙️ Configuração

3. O DoomTUI cria automaticamente o arquivo de configuração na primeira execução em:
    
    ```bash
    ~/.config/doomtui/doomtui.ini
    ```
    * O arquivo `doomtui.ini.example` do repositório não é lido pela aplicação, é apenas um exemplo.

4. Exemplo da estrutura padrão do **.ini:**

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

5. Execute o script principal a partir do terminal:

   ```bash
   doomtui.py
   ```
   * Use o Editor para configurar os diretórios dos seus ports, iwad, e pwad
   * Salve seu .ini
   * Selecione suas opções
   * Jogue à vontade

6. Atalhos de Teclado Principais:
   * ctrl-e: Abre o editor modal para alterar o arquivo doomtui.ini.
   * ctrl-v: Abre o modo somente leitura do arquivo doomtui.ini.
   * ctrl-q: Sai da aplicação.
   * Esc: Sai do editor e/ou visualizador

## 🗺️ (TODO)

7. Próximos Passos
   * [ ] Auto Refresh das seleções do iwad.
   * [ ] Salvar os parâmetros extras no .ini.
   * [ ] Adicionar checagem automática de atualizações do projeto.
   * [ ] Suporte a vários idiomas
   * [ ] Testar no Windows

## 📄 Licença

   * Este projeto é distribuído sob os termos da licença GNU General Public License v2.0 (GPLv2). 
   * Consulte o arquivo LICENSE para mais detalhes.
   * Cópias permitidas.
