import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import dotenv
import re
import logging

# Load environment variables
dotenv.load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Azure credentials and endpoint details
endpoint = os.getenv("AZURE_OAI_ENDPOINT")
deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

# Initialize the token provider
try:
    token_provider = DefaultAzureCredential()
    logging.debug("Token provider initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize token provider: {e}")

# Initialize Azure OpenAI client
try:
    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_deployment=deployment,
        azure_ad_token_provider=token_provider,
        api_version="2024-02-01"
    )
    logging.debug("Azure OpenAI client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Azure OpenAI client: {e}")

# Initial system message
system_message = {
    "role": "system",
    "content": "Sei un assistente virtuale chiamato Jonathan. Rispondi sempre nella stessa lingua della domanda dell'utente.",
}

def get_response(user_query):
    try:
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
                            "endpoint": os.getenv("AZURE_SEARCH_ENDPOINT"),
                            "index_name": os.getenv("AZURE_SEARCH_INDEX"),
                            "authentication": {
                                "type": "AzureActiveDirectory",
                                "client_id": os.getenv("AZURE_SEARCH_CLIENT_ID"),
                                "client_secret": os.getenv("AZURE_SEARCH_CLIENT_SECRET"),
                                "tenant_id": os.getenv("AZURE_SEARCH_TENANT_ID")
                            }
                        }
                    }
                ],
            }
        )

        # Extract the response content
        response_content = completion.choices[0].message.content

        # Remove references like [doc4] using regex
        cleaned_response_content = re.sub(r'\[doc\d+\]', '', response_content)
        
        return cleaned_response_content

    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return "There was an error processing your request."

def main():
    while True:
        # Prompt the user for input
        user_query = input("Per favore inserisci la tua domanda (o 'esci' per terminare): ")

        if user_query.lower() in ['esci', 'exit', 'quit']:
            print("Bye bye!")
            break

        # Get and print the response
        response = get_response(user_query)
        print("Response: " + "\n" + response + "\n")

if __name__ == '__main__':
    main()
