---
name: research-multi-perspective
description: Produce a research-grade, multi-voice analysis of a topic instead of a standard overview. Writes five distinct perspectives — practitioner, skeptic, economist, historian, academic — each speaking directly. Use when the user wants deep, contrarian, or multi-angle research on a subject, says "research-grade understanding", "give me different perspectives", "steelman both sides", or invokes /research-multi-perspective.
---

# Research: Multi-Perspective

The topic to research is provided as the skill argument. Treat everything passed in as `[TOPIC]`. If no topic was given, ask the user what they want researched before proceeding.

Respond to the following prompt, substituting the user's topic for `[TOPIC]`:

---

I want a research-grade understanding of: [TOPIC]

Don't give me the standard overview. Instead, write five
distinct perspectives on this topic from the following voices:

1. The PRACTITIONER who works with this every day.
   What do they know that books miss?

2. The SKEPTIC who believes the mainstream view is wrong.
   What's their strongest argument?

3. The ECONOMIST who follows the money.
   Who profits, who pays, what incentives are hidden?

4. The HISTORIAN who has seen this pattern before.
   What past event does this echo and what happened next?

5. The ACADEMIC who has read the underlying research.
   What do the studies actually say vs. what people
   claim they say?

Each perspective should be 4–6 sentences. Be specific.
No hedging. Write as if each voice were speaking directly.
