# Projeto LangChain (Assistente RAG)

Este repositório contém um exemplo de assistente RAG usando LangChain, ChromaDB e OpenAI.

## Preparação do ambiente (Windows PowerShell)

1. Crie e ative o virtual environment usando o script:

# Assistente RAG com LangChain

Este projeto é um exemplo completo de um Assistente RAG (Retrieval-Augmented Generation) construído com LangChain, ChromaDB e OpenAI.

O foco deste repositório é demonstrar:

- Como carregar documentos locais (PDFs) e indexá-los com embeddings em um vectorstore local (ChromaDB).
- Como montar uma cadeia RAG que recupera trechos relevantes e gera respostas com um LLM.
- Como agregar funcionalidades de memória (curto e longo prazo) e persistir experiências.
- Como contar tokens com precisão (usando `tiktoken`) e estimar custos por consulta.

## Principais diferenciais

1) Memória de curto prazo (contexto de conversa)

	- Implementado com `ConversationBufferMemory` do LangChain.
	- Mantém o histórico recente da conversa (ex.: últimas trocas de pergunta/resposta) e injeta esse contexto nas queries ao modelo, permitindo referências a mensagens anteriores.
	- Útil para manter fluidez em diálogos e preservar a coesão de seguida de mensagens.

2) Memória de longo prazo (experiência)

	- Armazenamento das "experiências" (pergunta + resposta) como textos indexados no vectorstore.
	- Permite que o sistema recupere situações passadas semelhantes e aprenda um histórico persistente de interações.
	- Ótimo para construir personalização ao longo do tempo (ex.: preferências do usuário, informações recorrentes).

3) Contagem de tokens e custo estimado

	- O utilitário `utills/token_counter.py` usa `tiktoken` para contar tokens de entrada e saída com precisão para o modelo especificado (por padrão `gpt-4o-mini`).
	- No código principal (`LangChain.py`) calculamos o custo estimado por interação usando os parâmetros:
	  - COST_INPUT_TOKEN = 0.000005 USD (ex.: $5 por 1M tokens de entrada)
	  - COST_OUTPUT_TOKEN = 0.000015 USD (ex.: $15 por 1M tokens de saída)
	- Essas taxas são exemplos e devem ser ajustadas conforme o modelo e plano real que você utiliza.

## Estrutura do projeto

- `LangChain.py` — fluxo principal: carregamento de documentos, indexação, criação do retriever, construção da cadeia conversacional e loop de interação.
- `utills/token_counter.py` — utilitário para contagem de tokens (funções `contar_tokens` e `contar_tokens_batch`).
- `utills/memories.py` — utilitários de memória: criação da `ConversationalRetrievalChain` com `ConversationBufferMemory` e função `salvar_memoria` para persistir experiências.
- `requirements.txt` — dependências recomendadas.
- `setup_venv.ps1` — script para criar virtual environment e instalar dependências (Windows PowerShell).
- `.env` — arquivo de variáveis de ambiente (coloque sua `OPENAI_API_KEY` aqui).

## Preparando o ambiente (Windows PowerShell)

1. Crie e instale dependências com o script:

```powershell
.\setup_venv.ps1
```

2. Ative o virtual environment em novas sessões:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Adicione sua chave OpenAI no `.env`:

```powershell
# abra .env e adicione sua chave
# OPENAI_API_KEY=sk-xxxx
```

4. Execute o assistente:

```powershell
python .\LangChain.py
```

