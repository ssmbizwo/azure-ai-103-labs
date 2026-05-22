# Lab 1.4 — Monitoring, tracing & cost telemetry

## What I built
- App Insights resource `appi-ai103` (workspace-based, ingestionMode=LogAnalytics).
  Required registering providers `microsoft.operationalinsights` + `microsoft.insights`.
- `traced_batch.py`: 20 chat calls, each wrapped in an OpenTelemetry span
  (`chat_call`) tagged with prompt_chars, prompt/completion/total tokens, latency_ms.
- Telemetry shipped via `configure_azure_monitor()` -> Azure Monitor exporter.

## Proven working
- Exporter debug log showed `Transmission succeeded: Items accepted` with HTTP 200.
- Confirmed instrumentation + transmission independent of query-side delay.

## Key lesson: "accepted" != "queryable"
Ingestion endpoint returns 200 the instant data is accepted, but a backend
pipeline (esp. workspace-based, esp. first ingest) delays KQL visibility by
~2-30 min. Debug order: confirm client transmission first, THEN wait on query.

## Span -> table mapping (Azure Monitor)
- SpanKind SERVER/CONSUMER -> requests
- SpanKind CLIENT/PRODUCER/INTERNAL -> dependencies
- `start_as_current_span` defaults to INTERNAL, so chat_call lands in `dependencies`.

## KQL to run once data surfaces
### Summary (count, total tokens, avg + p95 latency)
dependencies
| where name == 'chat_call'
| extend total_tokens = toint(customDimensions.total_tokens), latency_ms = todouble(customDimensions.latency_ms)
| summarize calls=count(), total_tokens=sum(total_tokens), avg_latency_ms=round(avg(latency_ms),0), p95_latency_ms=round(percentile(latency_ms,95),0)

### Per-call breakdown
dependencies
| where name == 'chat_call'
| extend prompt_tokens=toint(customDimensions.prompt_tokens), completion_tokens=toint(customDimensions.completion_tokens), total_tokens=toint(customDimensions.total_tokens), latency_ms=todouble(customDimensions.latency_ms)
| project timestamp, prompt_tokens, completion_tokens, total_tokens, latency_ms
| order by timestamp asc

### Token usage over time (5-min bins)
dependencies
| where name == 'chat_call'
| extend total_tokens = toint(customDimensions.total_tokens)
| summarize sum(total_tokens) by bin(timestamp, 5m)
