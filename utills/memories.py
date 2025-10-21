"""
Utilities de memória para o assistente RAG.
Contém:
- criação de ConversationBufferMemory e ConversationalRetrievalChain (memórias de contexto)
- função para salvar "memórias de experiência" (salva texto no vectorstore)

Dependências:
- langchain (ConversationBufferMemory, ConversationalRetrievalChain)

Este módulo foi criado para ser importado por `LangChain.py`.
"""

from typing import Any
# A instalação atual fornece os componentes de memória/clássicos em `langchain_classic`.
from langchain_classic.memory.buffer import ConversationBufferMemory
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain

# Observação: esse módulo assume que o caller fornecerá os objetos:
# - llm: o modelo (ex.: ChatOpenAI)
# - retriever: retriever vindo do vectorstore
# - embeddings: objeto de embeddings (ex.: OpenAIEmbeddings)
# - vectorstore: instância de Chroma (ou outro) com método add_texts


def criar_memory_chain(llm: Any, retriever: Any) -> ConversationalRetrievalChain:
    """Cria e retorna uma ConversationalRetrievalChain com memória de buffer.

    Args:
        llm: modelo de linguagem
        retriever: retriever que recupera documentos relevantes

    Returns:
        ConversationalRetrievalChain configurada com ConversationBufferMemory
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    return qa_chain


def salvar_memoria(pergunta: str, resposta: str, embeddings: Any, vectorstore: Any) -> None:
    """Salva uma experiência (pergunta+resposta) no vectorstore como texto com embedding.

    Nota: o vectorstore precisa expor um método `add_texts(list_of_texts)`.
    """
    texto = f"Pergunta: {pergunta}\nResposta: {resposta}"
    # gerar embedding (alguns objetos embeddings expõem embed_query ou similar)
    try:
        # se houver método embed_query
        if hasattr(embeddings, "embed_query"):
            embedding = embeddings.embed_query(texto)
        elif hasattr(embeddings, "embed_documents"):
            embedding = embeddings.embed_documents([texto])[0]
        else:
            embedding = None
    except Exception:
        embedding = None

    # Tenta adicionar o texto ao vectorstore (ignorando embedding explícito se não suportado)
    try:
        if hasattr(vectorstore, "add_texts"):
            vectorstore.add_texts([texto])
        elif hasattr(vectorstore, "from_documents"):
            # fallback: não temos um método direto; deixar para o caller
            pass
    except Exception:
        # falha ao salvar, não interromper a aplicação
        pass


if __name__ == "__main__":
    print("Módulo de memories carregado. Importe e use `criar_memory_chain` e `salvar_memoria` a partir de seu app.")
