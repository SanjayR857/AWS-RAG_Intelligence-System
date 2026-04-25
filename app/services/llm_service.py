from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain


from config import Config


class LLMService:
    def __init__(self, vector_store):
        self.vector_store = vector_store

        self.llm = AzureChatOpenAI(

            azure_endpoint=Config.Azure_OPENAI_ENDPOINT,
            api_key=Config.Azure_OPENAI_KEY,
            azure_deployment=Config.Azure_OPENAI_DEPLOYMENT,
            openai_api_version=Config.Azure_OPENAI_API_VERSION,
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
        )

    def get_response(self, query):
        try:
            response = self.chain.invoke(query)
            return response["answer"]

        except Exception as e:
            print(f"Error in LLMService: {e}")
            return "Sorry, I couldn't process your request at the moment."
