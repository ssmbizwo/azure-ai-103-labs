# Lab 1.5 — Responsible AI: content filters, blocklists, prompt shields

## What I built
- `filter_harness.py`: fires 10 prompts (5 benign, 2 blocklist, 3 jailbreak),
  reads `content_filter_results` on success, catches `BadRequestError` on a
  content-filter block and extracts the tripped category.
- Custom blocklist `lab15-blocklist` (term: "Contoso") via the management API.
- Custom RAI policy `lab15-policy`: inherits Microsoft.DefaultV2 content filters
  + Prompt Shields (jailbreak) + the custom blocklist for Prompt and Completion.
- Attached `lab15-policy` to the gpt-4o deployment.

## Proven results
- Default policy (Microsoft.DefaultV2) already BLOCKS jailbreaks via Prompt
  Shields -> all 3 jailbreak prompts returned `jailbreak=detected`.
- Benign prompts PASS with content_filter_results = all safe.
- Custom blocklist verified wired (GET shows Prompt+Completion, blocking=true).
  Blocklist enforcement on a live deployment propagates slowly; "Contoso"
  prompts flip to BLOCKED once propagated -> re-run harness to confirm.

## Key concepts
- DefaultV2 system policy can't be edited; to customize you create a UserManaged
  policy that sets `basePolicyName` AND a full `contentFilters` array (the API
  rejects null contentFilters), then attach it to the deployment.
- Content filter categories: hate, sexual, selfharm, violence (severity-based:
  Safe/Low/Medium/High) + Prompt Shields (jailbreak, indirect_attack) +
  protected material (text/code). Each can target Prompt and/or Completion.
- A blocked request raises HTTP 400 (content_filter); a passing request carries
  prompt_filter_results + per-choice content_filter_results annotations.

## Re-run later to see the blocklist block
python week-1-plan-and-manage/1-5-content-safety/filter_harness.py
