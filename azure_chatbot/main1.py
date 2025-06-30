import os
import re
import logging
from azure.identity import InteractiveBrowserCredential, get_bearer_token_provider
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Azure credentials and endpoint details
endpoint = "https://arkoopenai.openai.azure.com/"
deployment = "arkodeployment"

# Initialize the token provider using InteractiveBrowserCredential for testing
try:
    token_provider = get_bearer_token_provider(InteractiveBrowserCredential(), "https://cognitiveservices.azure.com/.default")
    logging.debug("Token provider initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize token provider: {e}")

# Initialize Azure OpenAI client
try:
    chat_model = AzureChatOpenAI(
        azure_endpoint=endpoint,
        azure_deployment=deployment,
        azure_ad_token_provider=token_provider,
        api_version="2024-02-01"
    )
    logging.debug("Azure OpenAI client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Azure OpenAI client: {e}")

# Initial system message
system_message = SystemMessage(
    content=(
        "You are a virtual assistant called Jonathan. "
        "Always respond in the same language as the user's question. "
        "If the user asks for your name, say your name is Jonathan."
    )
)

def get_response(user_query):
    try:
        logging.debug("Creating API call with user query: %s", user_query)
        
        messages = [
            system_message,
            HumanMessage(content=user_query),
        ]
        
        response = chat_model.invoke(messages)
        response_content = response["choices"][0]["message"]["content"]

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
