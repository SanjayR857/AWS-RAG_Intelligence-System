from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings

# from langchain_core.vectorstores import Chroma
from config import Config
import chromadb


class VectorStore:
    def __init__(self, collection_name):
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=Config.AZURE_EMBEDDING_DEPLOYMENT,
            azure_endpoint=Config.AZURE_EMBEDDING_ENDPOINT,
            api_key=Config.AZURE_EMBEDDING_KEY,
            api_version=Config.AZURE_EMBEDDING_API_VERSION,
            model=Config.AZURE_EMBEDDING_MODEL,

        )

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=Config.VECTOR_STORE_PATH,
        )

    def add_documents(self, documents):
        """Add documents to the vector store."""
        self.vector_store.add_documents(documents)

    def similarity_search(self, query, top_k=5):
        """Search for similar documents in the vector store."""
        return self.vector_store.similarity_search(query, k=top_k)

    def query(self, query_text, top_k=5):
        """Query the vector store for similar documents."""
        results = self.vector_store.similarity_search(query_text, k=top_k)
        return [
            doc.page_content for doc in results
        ]  # Return the list of similar documents

    def as_retriever(self):
        """Return the vector store as a retriever."""
        return self.vector_store.as_retriever()
