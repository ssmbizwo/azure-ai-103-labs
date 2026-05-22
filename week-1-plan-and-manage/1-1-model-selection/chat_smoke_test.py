"""Lab 1.1 smoke test: call chat + embedding models directly on the AI Services account."""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_AI_ENDPOINT"],
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
)

chat_deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
embed_deployment = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]

resp = client.chat.completions.create(
    model=chat_deployment,
    messages=[{"role": "user", "content": "Reply with exactly five words confirming you are working."}],
    max_tokens=20,
)
print("Chat reply :", resp.choices[0].message.content.strip())
print("Tokens used:", resp.usage.total_tokens)

emb = client.embeddings.create(
    model=embed_deployment,
    input="Foundry embedding smoke test.",
)
vector = emb.data[0].embedding
print(f"Embedding  : length={len(vector)}, first 3 values={vector[:3]}")

print("\n\u2713 Lab 1.1 complete \u2014 chat + embedding both reachable from Python.")
