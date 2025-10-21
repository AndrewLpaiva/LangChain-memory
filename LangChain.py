# =========================================
# Assistente RAG com LangChain
# Autor: Andrew Lucas de Paiva (Data Tenshi)
# =========================================

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
import os
from dotenv import load_dotenv
import time

# util de contagem de tokens
from utills.token_counter import contar_tokens
# util de memória
from utills.memories import criar_memory_chain, salvar_memoria

# =========================================
# 1. Configurações básicas
# =========================================
load_dotenv()  # carrega variáveis do .env

# Se desejar, mantenha OPENAI_API_KEY no .env. Caso contrário, defina no ambiente.
# Não sobrescreveremos a variável aqui para evitar expor a chave no código.

# Modelo e parâmetros de custo (em USD)
MODEL_NAME = "gpt-5-nano"
COST_INPUT_TOKEN = 0.000000005  # custo por token de entrada (~$0,05 / 1M tokens)
COST_OUTPUT_TOKEN = 0.0000004 # custo por token de saída (~$0,400 / 1M tokens)

# =========================================
# 2. Carregar os documentos
# =========================================
pdf_path = r"c:\Users\andre\OneDrive\Área de Trabalho\Mais-Esperto-Diabo.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# =========================================
# 3. Quebrar os textos em pedaços menores
# =========================================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # tamanho máximo de cada trecho
    chunk_overlap=150 # sobreposição entre trechos
)
docs_chunked = text_splitter.split_documents(documents)

# =========================================
# 4. Gerar embeddings e armazenar localmente
# =========================================
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs_chunked, embeddings, persist_directory="db_chroma")

# =========================================
# 5. Criar o retriever e o modelo de linguagem
# =========================================
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # busca os 3 trechos mais relevantes
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2,max_tokens=200)

# =========================================
# 6. Construir a cadeia RAG
# =========================================
# Usar cadeia conversacional com memória (se desejar manter conversa)
qa_chain = criar_memory_chain(llm=llm, retriever=retriever)

# =========================================
# 7. Interagir com o assistente
# =========================================
while True:
    query = input("\nPergunte algo sobre seus documentos (ou 'sair'): ")
    if query.lower() == "sair":
        break

    # contar tokens de entrada
    tokens_input = contar_tokens(query, modelo=MODEL_NAME)
    inicio = time.time()

    result = qa_chain({"query": query})

    tempo_resposta = time.time() - inicio
    resposta = result.get("result", "")
    tokens_output = contar_tokens(resposta, modelo=MODEL_NAME)

    # estimar custo
    custo = (tokens_input * COST_INPUT_TOKEN) + (tokens_output * COST_OUTPUT_TOKEN)

    print("\n🔍 Resposta:")
    print(resposta)
    print("\n📄 Fontes utilizadas:")
    for doc in result.get("source_documents", []):
        print("-", doc.metadata.get("source", "Desconhecida"))

    print("\n📊 Métricas:")
    print(f"Tokens entrada: {tokens_input}")
    print(f"Tokens saída: {tokens_output}")
    print(f"Custo estimado: US$ {custo:.6f}")
    print(f"Tempo de resposta: {tempo_resposta:.2f}s")
    print("-" * 60)
