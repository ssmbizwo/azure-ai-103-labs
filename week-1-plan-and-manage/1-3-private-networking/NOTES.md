# Lab 1.3 — Private networking (lighter hands-on)

## What I built
- VNet `vnet-ai103` (10.0.0.0/16) with subnet `snet-pe` (10.0.1.0/24).
- Private Endpoint `pe-ai103` on the AI Services account (group-id `account`),
  auto-approved because I own the resource. Got 3 private IPs:
  - cognitiveservices.azure.com -> 10.0.1.4
  - openai.azure.com            -> 10.0.1.5
  - services.ai.azure.com       -> 10.0.1.6

## What I proved
- Set `publicNetworkAccess=Disabled` -> smoke test from laptop failed with
  403 "Public access is disabled. Please configure private endpoint."
- Set it back to `Enabled` -> smoke test passed again.
- Re-enabling worked from the laptop even while data-plane public access was
  off => control plane (ARM) is never gated by the resource's network rules.

## Exam mental model
Private AI service = three pieces together:
1. **Private Endpoint** — gives the resource a private IP in the VNet.
2. **Private DNS Zone** (privatelink.*.azure.com) — makes the FQDN resolve to
   that private IP from inside the VNet. (Not set up here; needs a VM to test.)
3. **Public network access = Disabled** — closes the public door.

Know the difference:
- **Private Endpoint** = private IP, traffic over Microsoft backbone, most secure.
- **Service Endpoint** = traffic still to public IP but over Azure backbone; VNet identity allowed.
- **Selected networks / IP allowlist** = simplest, public endpoint restricted to listed IPs.

Connection approval can be **Approved** (you own it) or **Pending** (cross-team/tenant).
