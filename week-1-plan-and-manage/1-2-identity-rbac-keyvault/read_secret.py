"""Lab 1.2: retrieve the AI Services key from Key Vault using Entra ID auth (no key in code)."""
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = "https://kv-projai10298135535608.vault.azure.net/"

client = SecretClient(vault_url=VAULT_URL, credential=DefaultAzureCredential())
secret = client.get_secret("ai-services-key")

print("Secret retrieved from Key Vault via DefaultAzureCredential")
print(f"  Name        : {secret.name}")
print(f"  Value length: {len(secret.value)} chars")
print(f"  Preview     : {secret.value[:4]}... (masked)")
print("\n\u2713 Lab 1.2 complete \u2014 key-less app + secret stored in Key Vault.")
