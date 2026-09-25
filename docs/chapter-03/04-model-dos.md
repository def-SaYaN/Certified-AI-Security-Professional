---
tags:
  - Chapter 3
  - OWASP
---

# LLM04 — Model Denial of Service

!!! objective "In this section"
    - How DoS against a model differs from DoS against a network or application
    - Context windows and how attackers exhaust them
    - "Denial of wallet" — a genuinely new attack class
    - Mitigations, and why they must be measured in tokens

---

## What is it?

> **Model denial of service** is causing an LLM application to consume excessive resources —
> degrading service for legitimate users, or running up crippling costs.

The unusual feature of this category is that **availability and cost are the same attack
surface**. In traditional web security, serving an extra request is essentially free; in AI, every
request costs metered compute. That changes the economics completely.

---

## DoS on networks, applications, and models

Three levels, each with a different mechanism:

| Level | Mechanism | Example | Cost to attacker |
|---|---|---|---|
| **Network** | Flood with traffic | Volumetric DDoS | High — needs bandwidth/botnet |
| **Application** | Trigger expensive operations | Slow database queries, zip bombs | Medium |
| **Model** | Trigger expensive **inference** | Huge context, long generation, recursive tools | **Very low** |

!!! danger "The economics strongly favour the attacker"
    A single crafted request can consume orders of magnitude more compute than a normal one, and
    cost the attacker nothing but the time to type it.

    Traditional DDoS needs a botnet. Model DoS may need one laptop and a well-chosen prompt. This
    asymmetry is what makes the category worth its own entry.

---

## Context windows and exhaustion

From section 2.1: a model can only consider a limited amount of text at once — its **context
window**, measured in tokens. Everything must fit: system prompt, conversation history, retrieved
documents, and the user's input.

Attackers exploit this in several ways:

<dl class="caisp-terms" markdown>

<dt>Direct context flooding</dt>
<dd>Send an enormous input that fills the window. Processing cost typically scales steeply with
context length, so long inputs are disproportionately expensive.</dd>

<dt>Token inflation</dt>
<dd>You demonstrated this in <strong>Lab 2.2</strong>: text that is short in <em>characters</em>
but dense in <em>tokens</em> — unusual Unicode, rare scripts, no word boundaries. A message that
looks small can cost many times its apparent size.</dd>

<dt>History flooding in conversation</dt>
<dd>Because the entire transcript is re-sent each turn (Lab 1.1), an attacker who pads early turns
makes <em>every subsequent turn</em> expensive. The cost compounds across the session.</dd>

<dt>Forcing long generations</dt>
<dd>Prompts engineered to produce maximum-length output. Generation is usually more expensive per
token than input processing, so this is efficient for the attacker.</dd>

<dt>Recursive or looping tool calls</dt>
<dd>In agentic systems, an injected instruction can send the model into a loop of tool calls, each
one an inference. This is one of the most expensive failure modes available.</dd>

<dt>Context squeezing as a security bypass</dt>
<dd>A subtler variant: fill the context so that the <em>system prompt</em> is pushed out or
truncated. The model then operates without its safety instructions. This turns a resource attack
into a guardrail bypass.</dd>

</dl>

!!! warning "That last one deserves emphasis"
    **Context exhaustion can be a path to prompt injection.** If your application silently drops
    the oldest context (as many do, including the trimming logic in Lab 1.1) an attacker who
    floods the window may evict your system prompt entirely.

    When you assess a system, ask: *what gets dropped when the context is full, and is the system
    prompt protected from eviction?*

---

## Denial of wallet

A genuinely novel attack class with no real traditional equivalent.

> **Denial of wallet** is deliberately driving up a victim's metered costs, rather than trying to
> take the service down.

Because hosted LLMs bill per token, an attacker who can send requests can generate real financial
liability. Consequences range from an unpleasant invoice to service suspension when a spending cap
is hit — at which point the cost attack *becomes* an availability attack.

!!! info "Why this catches teams out"
    Traditional capacity planning assumes requests are cheap and roughly uniform. LLM requests are
    expensive and wildly variable — one request might cost 100× another. Teams that rate-limit "10
    requests per minute" without considering *size* have not limited cost at all.

---

## Mitigating model denial of service

This category is genuinely fixable with disciplined engineering.

<dl class="caisp-terms" markdown>

<dt>Rate limit on tokens, not requests</dt>
<dd>The single most important control, and the most commonly botched. Count what you are billed
for.

```python
# WRONG — a request is not a unit of cost
if requests_this_minute > 10: reject()

# RIGHT — tokens are the unit of cost
if tokens_this_hour + len(tokenizer.encode(user_input)) > TOKEN_BUDGET:
    reject()
```

</dd>

<dt>Cap input length in tokens</dt>
<dd>Validate the tokenized length before sending anything to the model. A character-based cap
under-counts token-dense input (Lab 2.2).</dd>

<dt>Cap output length</dt>
<dd>Set <code>max_tokens</code> on every generation. Never let a model generate unbounded
output.</dd>

<dt>Per-user quotas and spend caps</dt>
<dd>Budget per user, per tenant, and globally. Combine with hard provider-side spending limits so
a runaway attack cannot produce an unbounded bill.</dd>

<dt>Cost monitoring and alerting</dt>
<dd>Alert on anomalous spend <em>in real time</em>. Discovering a denial-of-wallet attack on next
month's invoice is discovering it far too late.</dd>

<dt>Limit agent loops</dt>
<dd>Hard-cap the number of tool calls or reasoning steps per request. Agentic systems need a
circuit breaker.</dd>

<dt>Protect the system prompt from eviction</dt>
<dd>When trimming context, preserve the system prompt. Truncate history, never your
instructions.</dd>

<dt>Require authentication for expensive operations</dt>
<dd>Anonymous access to a costly model is an invitation. At minimum, authenticate before allowing
large contexts or long generations.</dd>

</dl>

!!! tip "The one-line exam answer"
    **Measure and limit in tokens, not characters or requests** — because tokens are the unit of
    both cost and context consumption.

---

!!! question "Check your understanding"
    ??? success "Why is limiting input by character count insufficient?"
        Because cost and context are measured in tokens, and token density varies enormously.
        Non-English text, unusual Unicode, and rare scripts produce far more tokens per character
        (Lab 2.2), so a character cap can permit input many times more expensive than intended.

    ??? success "What is denial of wallet and why has it no real traditional equivalent?"
        Deliberately driving up a victim's metered inference costs. Traditional web requests are
        essentially free to serve, so cost was never the target; LLM requests consume billed
        compute, making the victim's budget a viable attack surface.

    ??? success "How can a resource-exhaustion attack become a guardrail bypass?"
        If the application drops the oldest context when the window fills, an attacker who floods
        the context can evict the system prompt, leaving the model operating without its safety
        instructions.

---

<div class="caisp-cards">
<a class="caisp-card" href="05-supply-chain.md">
  <span class="caisp-kicker">Next · LLM05</span>
  <span class="caisp-card-title">Supply Chain Vulnerabilities</span>
  <span class="caisp-card-text">Models and datasets as untrusted dependencies.</span>
</a>
</div>
