import os
from dotenv import load_dotenv


load_dotenv(
    override=True, dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env")
)


class Config:
    Azure_OPENAI_KEY = os.getenv("Azure_OPENAI_KEY")
    Azure_OPENAI_ENDPOINT = os.getenv("Azure_OPENAI_ENDPOINT")
    Azure_OPENAI_DEPLOYMENT = os.getenv("Azure_OPENAI_DEPLOYMENT")
    Azure_OPENAI_API_VERSION = os.getenv("Azure_OPENAI_API_VERSION")
    AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")


    AZURE_EMBEDDING_ENDPOINT = os.getenv("AZURE_EMBEDDING_ENDPOINT")
    AZURE_EMBEDDING_KEY = os.getenv("AZURE_EMBEDDING_KEY")
    AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    AZURE_EMBEDDING_API_VERSION = os.getenv("AZURE_EMBEDDING_API_VERSION")
    AZURE_EMBEDDING_MODEL = os.getenv("AZURE_EMBEDDING_MODEL")


    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

    VECTOR_STORE_PATH = "chromedb"
