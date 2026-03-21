from google import genai
import json

# COLOQUE A SUA CHAVE AQUI DENTRO DAS ASPAS 👇
CHAVE_API = "AIzaSyD7xtOKH9yo59ffRBK_-Ng4vOimGQ1xYn4"

# Novo jeito de autenticar na biblioteca nova
client = genai.Client(api_key=CHAVE_API)

def gerar_trinca_quiz_mania(desc_cristianismo, desc_musculacao, desc_musica):
    print("🤖 Injetando links e gerando a trinca de ouro...")
    
    prompt = f"""
    Aja como um roteirista viral de YouTube Shorts e TikTok.
    Você deve gerar um array JSON contendo EXATAMENTE 3 quizzes nas seguintes categorias e ordem:
    1º: Cristianismo (Fatos bíblicos gerais para jovens).
    2º: Musculação (Treino, nutrição e hipertrofia).
    3º: Música (Teoria básica, violão e instrumentos).

    REGRAS OBRIGATÓRIAS (SIGA À RISCA):
    1. Retorne APENAS o JSON puro. Sem blocos de código Markdown (```json).
    2. Cada quiz deve ter EXATAMENTE 5 perguntas.
    3. Cada pergunta deve ter EXATAMENTE 3 opções de resposta (índices 0, 1 e 2).
    4. A chave "correta" deve ser um número inteiro (0, 1 ou 2) indicando o índice da resposta certa.
    5. Distribua bem as respostas certas (NÃO coloque todas as respostas corretas na mesma posição, evite padrões).
    6. As descrições devem ser EXATAMENTE as seguintes, mapeadas por tema:
       - Para o quiz de Cristianismo: "{desc_cristianismo}"
       - Para o quiz de Musculação: "{desc_musculacao}"
       - Para o quiz de Música: "{desc_musica}"

    Siga EXATAMENTE esta estrutura JSON para a resposta:
    [
      {{
        "titulo": "Título Chamativo com Emojis 🚀",
        "descricao": "Texto da descrição que eu te passei acima",
        "perguntas": [
          {{
            "pergunta": "Texto da pergunta?",
            "opcoes": ["Opção 0", "Opção 1", "Opção 2"],
            "correta": 1
          }}
        ]
      }}
    ]
    """
    
    try:
        # Novo jeito de chamar o modelo
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        texto_limpo = resposta.text.strip()
        
        if texto_limpo.startswith("```json"):
            texto_limpo = texto_limpo.replace("```json", "", 1)
        if texto_limpo.endswith("```"):
            texto_limpo = texto_limpo.rsplit("```", 1)[0]
            
        lista_de_roteiros = json.loads(texto_limpo.strip())
        return lista_de_roteiros
        
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        return None

# ==========================================
# 🧪 ÁREA DE TESTE ISOLADO
# ==========================================
if __name__ == "__main__":
    print("Iniciando teste isolado da API do Gemini (Nova Versão)...")
    
    # Simulando os textos que virão lá do seu app.py
    teste_cristianismo = "Comente quantas acertou! 👇\nCOMPRE SEU VIOLÃO AQUI: [https://meli.la/1ym5joa](https://meli.la/1ym5joa)"
    teste_musculacao = "Comente quantas acertou! 👇\nCREATINA PURA AQUI: [https://sua-loja.com/creatina](https://sua-loja.com/creatina)"
    teste_musica = "Comente quantas acertou! 👇\nCOMPRE SEU VIOLÃO AQUI: [https://meli.la/1ym5joa](https://meli.la/1ym5joa)"
    
    # Dispara a função
    resultado_json = gerar_trinca_quiz_mania(teste_cristianismo, teste_musculacao, teste_musica)
    
    if resultado_json:
        print("\n✅ DEU BOM! Olha a trinca de ouro gerada automaticamente:")
        # Imprime o JSON bonitão na tela
        print(json.dumps(resultado_json, indent=2, ensure_ascii=False))
    else:
        print("\n❌ Algo deu errado. Verifique se a sua chave de API está correta lá em cima.")