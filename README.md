Fala, João! Com todas essas atualizações parrudas que a gente fez hoje (Motor infinito da Microsoft, Renderização Turbo e a Interface Aurora Glass em Lote), a documentação antiga ficou totalmente defasada mesmo.

Preparei o seu `README.md` no padrão ouro do GitHub. Ele já reflete que o projeto agora é 100% gratuito (sem ElevenLabs), processa em lote e usa multi-threading para voar na renderização. Também deixei os exemplos de temas alinhados com os que você configurou (Cristianismo, Musculação e Música).

É só copiar o bloco inteiro abaixo e colar no seu arquivo **`README.md`** lá no repositório:

---

# 🎬 Quiz Mania - Fábrica Automática de Vídeos

## 📖 Visão Geral

O **Quiz Mania** é um sistema automatizado para geração de vídeos curtos em lote (formato TikTok/Shorts/Reels) focado em quizzes interativos. O projeto recebe roteiros em formato JSON e renderiza, de ponta a ponta, vídeos dinâmicos contendo narração gerada por IA (100% gratuita e ilimitada), efeitos sonoros, trilha sonora mixada, temporizador, botões interativos e uma tela final de Call-to-Action (CTA).

O projeto foi arquitetado com foco em otimização extrema, utilizando processamento multi-thread, sistema inteligente de cache de áudio e uma interface web moderna (estilo *Aurora Glass*) para produção industrial de conteúdo.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12+**: Linguagem base da arquitetura.
* **Streamlit**: Framework utilizado para criar a Interface Gráfica Web em formato de linha de produção.
* **MoviePy**: Biblioteca principal para edição e composição de vídeo e áudio não-linear.
* **Pillow (PIL)**: Renderização gráfica nativa das interfaces do vídeo (cards, textos auto-ajustáveis, suporte a emojis do Windows, botões e cronômetro).
* **Edge TTS (Microsoft)**: Geração de locução Text-to-Speech (TTS) com vozes de alta retenção, de forma ilimitada e sem necessidade de chaves de API.
* **Git / GitHub**: Controle de versão do código.

## ✨ Funcionalidades Principais

* **🏭 Produção em Lote (Batch Processing):** Interface com abas que permite colar até 3 roteiros diferentes e processá-los sequencialmente com um único clique.
* **🎙️ Locução Ilimitada (Zero Custo):** Integração assíncrona com o Edge TTS da Microsoft, garantindo narrações dinâmicas sem limites de caracteres ou mensalidades.
* **⚡ Renderização Turbo (Multi-threading):** Otimização profunda no motor do MoviePy (`preset=ultrafast` e liberação de múltiplos núcleos da CPU) para reduzir drasticamente o tempo de compilação do vídeo.
* **🎨 Interface *Aurora Glass*:** Painel Dark Mode com design de vidro fosco, gradientes animados e feedback visual completo (barras de progresso e notificações toast).
* **🧠 Cache Inteligente de Áudio (Hash MD5):** O sistema assina e verifica o JSON. Se a pergunta não mudou, ele reaproveita o áudio local instantaneamente, poupando a rede.
* **🔁 Looping de Fundo Infinito:** Algoritmo que clona vídeos curtos de fundo para cobrir toda a extensão do quiz, evitando congelamentos.
* **🔊 Audio Mixdown Profissional:** Sincronização automática entre a locução, efeitos (tic-tac, acerto) e a música de fundo com volume balanceado.

## 📂 Estrutura do Projeto

```text
📦 quiz_ai/
 ┣ 📂 assets/
 ┃ ┣ 📂 audio/               # Cache inteligente dos áudios gerados pelo Edge TTS
 ┃ ┣ 📂 videos_prontos/      # Linha de montagem final (mp4)
 ┃ ┣ 📜 background_cristao.mp4
 ┃ ┣ 📜 background_minecraft.mp4
 ┃ ┣ 📜 background_musculacao.mp4
 ┃ ┣ 📜 background_musica.mp4
 ┃ ┣ 📜 background_music.mp3 # Trilha sonora base
 ┃ ┣ 📜 correct.mp3          # Efeito sonoro de acerto
 ┃ ┗ 📜 ticking.mp3          # Efeito sonoro de tempo
 ┣ 📜 .gitignore             # Regras de exclusão (exclui arquivos de mídia pesados do repo)
 ┣ 📜 app.py                 # Ponto de entrada: Interface Web Multi-Aba (Streamlit)
 ┣ 📜 video_generator.py     # Motor Gráfico: Composição MoviePy, Pillow e Otimização de Threads
 ┗ 📜 voice_generator.py     # Módulo de Áudio: Integração Edge TTS Assíncrono e Cache

```

## 🚀 Como Executar o Projeto

### 1. Instale as dependências

Certifique-se de ter o Python instalado. No terminal do seu projeto, execute:

```bash
pip install moviepy pillow numpy edge-tts streamlit

```

*(Nota: O sistema foi atualizado para Edge TTS, dispensando o uso do `python-dotenv` e contas pagas).*

### 2. Inicie a Fábrica Local

Para abrir a interface do painel *Aurora Glass*, execute o comando abaixo no terminal:

```bash
python -m streamlit run app.py

```

O painel abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## 📝 Uso Diário (A Linha de Montagem)

1. Solicite ao seu LLM favorito (ex: Gemini) a geração de roteiros de perguntas no formato JSON padrão.
2. Na interface web, navegue pelas abas **Vídeo 01, 02 e 03** e cole os respectivos JSONs.
3. Escolha o tema visual correspondente (Cristão, Musculação, Música ou Minecraft) para cada aba.
4. Clique em **🚀 INICIAR PRODUÇÃO**.
5. Acompanhe a barra de progresso unificada. O sistema gerará os áudios e vídeos simultaneamente. Os arquivos finais estarão disponíveis direto no player da tela e salvos na pasta `assets/videos_prontos/`.

---

---
