import os
import openai
import dotenv
import re

dotenv.load_dotenv()

# Load environment variables
endpoint = os.environ.get("AZURE_OAI_ENDPOINT")
api_key = os.environ.get("AZURE_OAI_KEY")
deployment = os.environ.get("AZURE_OAI_DEPLOYMENT")
search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
search_index = os.environ.get("AZURE_SEARCH_INDEX")
search_key = os.environ.get("AZURE_SEARCH_KEY")

# Initialize the OpenAI client
client = openai.AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

# Initial system message
system_message = {
    "role": "system",
    "content": "Sei un assistente virtuale chiamato Jonathan. Rispondi sempre nella stessa lingua della domanda dell'utente.",
}

def get_response(user_query):
    completion = client.chat.completions.create(
        model=deployment,
        temperature=0.5,
        max_tokens=1000,
        messages=[
            system_message,
            {
                "role": "user",
                "content": user_query,
            },
        ],
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": search_index,
                        "authentication": {
                            "type": "api_key",
                            "key": search_key,
                        }
                    }
                }
            ],
        }
    )

    # Ex
