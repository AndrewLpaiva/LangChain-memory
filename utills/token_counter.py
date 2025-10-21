"""
Utilities para contagem de tokens.

Fornece:
- obter_encoder(modelo): retorna um encoder tiktoken (com fallback)
- contar_tokens(texto, modelo): conta tokens de um texto
- contar_tokens_batch(texts, modelo): conta tokens para vários textos

Dependência recomendada: tiktoken
"""

from typing import List
import tiktoken

DEFAULT_MODEL = "gpt-4o-mini"


def obter_encoder(modelo: str = DEFAULT_MODEL):
    """Tenta obter um encoder para o modelo especificado. Usa fallback quando necessário."""
    try:
        return tiktoken.encoding_for_model(modelo)
    except Exception:
        try:
            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            class SimpleEncoder:
                def encode(self, text: str):
                    # fallback: cada caractere como 1 token (aproximação)
                    return list(text)
            return SimpleEncoder()


def contar_tokens(texto: str, modelo: str = DEFAULT_MODEL) -> int:
    """Retorna o número de tokens no texto para o modelo especificado."""
    enc = obter_encoder(modelo)
    try:
        return len(enc.encode(texto))
    except Exception:
        return len(texto)


def contar_tokens_batch(texts: List[str], modelo: str = DEFAULT_MODEL) -> List[int]:
    """Conta tokens para uma lista de textos reutilizando o encoder."""
    enc = obter_encoder(modelo)
    resultados: List[int] = []
    for t in texts:
        try:
            resultados.append(len(enc.encode(t)))
        except Exception:
            resultados.append(len(t))
    return resultados


if __name__ == "__main__":
    exemplo = "Este é um texto de exemplo para contar tokens."
    print("Modelo padrão:", DEFAULT_MODEL)
    print("Texto:", exemplo)
    print("Tokens (contar_tokens):", contar_tokens(exemplo))
    lista = [exemplo, "Outro texto mais longo para testar a função em batch."]
    print("Tokens (batch):", contar_tokens_batch(lista))