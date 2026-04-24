import os 
from dotenv import load_dotenv


load_dotenv()

class Config:

    Azure_OPENAI_KEY = os.getenv("Azure_OPENAI_KEY")
    Azure_OPENAI_ENDPOINT = os.getenv("Azure_OPENAI_ENDPOINT")
    Azure_OPENAI_DEPLOYMENT = os.getenv("Azure_OPENAI_DEPLOYMENT")
    Azure_OPENAI_API_VERSION = os.getenv("Azure_OPENAI_API_VERSION")
    AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

    VECTOR_STORE_PATH = "chromedb"