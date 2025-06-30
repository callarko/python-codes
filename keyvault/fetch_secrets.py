import os
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Set Key Vault URL
KEY_VAULT_URL = "https://arkokeyvault.vault.azure.net/"

# Authenticate using DefaultAzureCredential (supports managed identity or service principal)
credential = DefaultAzureCredential()

# Create a SecretClient
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

# Fetch Client ID and Client Secret from Key Vault
client_id = client.get_secret("ClientId").value
client_secret = client.get_secret("ClientSecret").value
tenant_id = "9329c02a-4050-4798-93ae-b6e37b19af6d"  # Replace with your Tenant ID

print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")

# OAuth2 token endpoint
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

# Define the request body for the token request
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://vault.azure.net/.default'
}

# Make the token request
response = requests.post(token_url, data=token_data)

# Check if the request was successful
if response.status_code == 200:
    token = response.json().get('access_token')
    print(f"Access Token: {token}")
else:
    print(f"Failed to get access token: {response.status_code}, {response.text}")
