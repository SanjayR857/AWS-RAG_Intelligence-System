from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain


from config import Config

class LLMService: 

    def __init__(self):

        self.llm = AzureChatOpenAI(
            azure_deployment=Config.Azure_OPENAI_DEPLOYMENT,
            openai_api_version=Config.Azure_OPENAI_API_VERSION,
            temperature=0.0,
        )

        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-ada-002",
            azure_endpoint=Config.Azure_OPENAI_ENDPOINT,
            api_key=Config.Azure_OPENAI_KEY,
            api_version=Config.Azure_OPENAI_API_VERSION,
            chunk_size=1
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True)
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm, 
            retriever=None,  # You can set up a retriever here
            memory=self.memory
        )
        
    
    def get_response(self, query):
        """Get a response from the LLM based on the user's query."""
        try:
            response = self.chain.run(query)
            return response['answer']
        
        except Exception as e:
            print(f"Error in LLMService: {e}")
            return "Sorry, I couldn't process your request at the moment."

















































# llm = AzureChatOpenAI(
#         azure_deployment="gpt-4o",
#         openai_api_version="2024-12-01-preview",
#         temperature=0.0,
#     )


# embeddings = AzureOpenAIEmbeddings(
#         azure_deployment="text-embedding-ada-002",
#         azure_endpoint=os.environ["AZURE_OPENAI_EMBEDDINGS_ENDPOINT"],
#         api_key=os.environ["AZURE_OPENAI_EMBEDDINGS_KEY"],
#         api_version=os.environ["AZURE_OPENAI_EMBEDDINGS_API_VERSION"],
#         chunk_size=1

#     )