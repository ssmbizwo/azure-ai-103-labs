"""Lab 1.4: fire a batch of chat calls, each wrapped in an OpenTelemetry span
tagged with prompt size, token usage, and latency -> Application Insights."""
import os, time, random
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

load_dotenv()

configure_azure_monitor(connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"])
tracer = trace.get_tracer("ai103.lab14")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_AI_ENDPOINT"],
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
)
chat_deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

topics = ["cloud computing", "machine learning", "databases", "networking",
          "containers", "DNS", "encryption", "APIs", "RAG", "embeddings"]
random.seed(42)
prompts = []
for _ in range(20):
    k = random.randint(1, 6)
    picked = random.sample(topics, k)
    prompts.append("In one short sentence each, describe: " + ", ".join(picked) + ".")

print(f"Firing {len(prompts)} chat calls...\n")
for i, p in enumerate(prompts, 1):
    with tracer.start_as_current_span("chat_call") as span:
        t0 = time.time()
        resp = client.chat.completions.create(
            model=chat_deployment,
            messages=[{"role": "user", "content": p}],
            max_tokens=150,
        )
        latency_ms = (time.time() - t0) * 1000
        u = resp.usage
        span.set_attribute("prompt_chars", len(p))
        span.set_attribute("prompt_tokens", u.prompt_tokens)
        span.set_attribute("completion_tokens", u.completion_tokens)
        span.set_attribute("total_tokens", u.total_tokens)
        span.set_attribute("model", chat_deployment)
        span.set_attribute("latency_ms", round(latency_ms, 1))
    print(f"[{i:2}/20] chars={len(p):3}  tokens={u.total_tokens:3}  latency={latency_ms:6.0f}ms")

print("\nFlushing telemetry to Application Insights...")
trace.get_tracer_provider().force_flush()
time.sleep(5)
print("Done. Data will appear in App Insights in ~1-3 minutes.")
