from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbedding(EmbeddingFunction):
    def __call__(self, texts: Documents) -> Embeddings:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(texts).tolist()
        return embeddings
