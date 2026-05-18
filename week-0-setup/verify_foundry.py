import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai = client.get_openai_client()
print("✓ Foundry project client built")
print(f"  Base URL: {openai.base_url}")
print(f"  API version: {openai._api_version if hasattr(openai, '_api_version') else 'default'}")
print("✓ Authentication chain works")
