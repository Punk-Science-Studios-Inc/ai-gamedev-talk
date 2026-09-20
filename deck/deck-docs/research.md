# Research for the deck (fetched 2026-09-20)

## Numbers for slides

| Metric | Value | Source |
|---|---|---|
| Models listed on OpenRouter API (incl. `:free`/`:batch` variants) | 446 (~400 base) | https://openrouter.ai/api/v1/models |
| New OpenRouter entries, last 4 weeks | 39 (~10/week); 74 in 8 wks; 114 in 12 wks | same API, `created` timestamps |
| Hugging Face public models | 3,080,517 | https://huggingface.co/models |
| HF growth | ~2,700–3,000 new models/day; 3M milestone 18 Aug 2026 | https://huggingface.co/blog/ivanfioravanti/three-million-models-and-counting |
| herdr GitHub stars | 39.8k, Apache-2.0 | https://github.com/herdrdev/herdr |
| Fly.io cheapest VM | shared-cpu-1x 256MB, $2.02/mo | https://fly.io/docs/about/pricing/ |
| Muse Code plans | $5 / $15 / $50 per month | https://developer.meta.com/ai/products/muse-code/ |
| Command A+ | 218B total / 25B active MoE, 20 May 2026 | https://cohere.com/blog/command-a-plus |
| North Mini Code | 30B / 3B active, Apache-2.0, runs locally | https://cohere.com/blog/north-mini-code |

## OpenRouter `auto`
Docs: https://openrouter.ai/docs/features/model-routing. "The Auto Router automatically selects the best model for your prompt, powered by the wisdom of the market": routes by task type and what the community spends on over a trailing 7-day window. Recent adds: anthropic/claude-fable-5.1 (1 Sep), openai/gpt-6-astra (4 Sep), meta/muse-spark-1.3 (2 Sep), qwen/qwen3.8-max-0902, z-ai/glm-5.3-flashx (18 Sep).

## Canadian models
- Cohere (Toronto), Command family: Command A+ (May 2026), Command A (111B open-weights), Command A Reasoning / Vision / Translate, Command R7B, R/R+. https://docs.cohere.com/docs/models
- Cohere North Mini Code: 30B MoE / 3B active, Apache-2.0, agentic coding, free on OpenRouter as cohere/north-mini-code:free.
- Vector / Mila / Amii: national AI institutes under "AI for All" (4 Jun 2026); no 2026 foundation model launch found.

## Chinese open-weights flagships (live on OpenRouter 2026-09-20)
- Qwen (Alibaba): Qwen3.8 Max (2.4T MoE, text+image+video in); Qwen3.8-27B dense.
- DeepSeek: DeepSeek V4 Pro (1.6T total / 49B active, 1M ctx); V4.1 Flash (10 Sep 2026).
- Kimi (Moonshot): Kimi K3 (2.8T open-weight multimodal reasoning).
- GLM (Zhipu / Z.ai): GLM-5.3 (1M ctx).

## Harnesses
- Claude Code (Anthropic): https://code.claude.com/docs/en/overview. Terminal + IDE + desktop + web. Anthropic models only (via API, Bedrock, Vertex, Foundry, gateway). No local models. Skills, subagents, hooks, MCP, plugins. Pro $20 / Max $100 / $200 or API PAYG.
- Codex CLI (OpenAI): https://github.com/openai/codex (Apache-2.0). Terminal + IDE. ChatGPT plan or API key; OpenAI models. Skills, MCP, plugins. Local gpt-oss via Ollama (secondary).
- OpenCode (Anomaly, formerly SST): https://opencode.ai. Terminal TUI. 75+ providers incl. OpenRouter, Ollama, LM Studio, llama.cpp. Agents/skills/MCP. Free OSS; optional Zen; OpenCode Go $10/mo.
- Muse Code (Meta): https://developer.meta.com/ai/products/muse-code/. Terminal coding agent, launched 5–6 Aug 2026, Muse Spark 1.2/1.3 (closed, cloud). Locked to Meta models. Contributor tier trains on your data. $5/$15/$50 per month.
- Pi (Earendil Inc., MIT): https://pi.dev, https://github.com/earendil-works/pi. Terminal TUI, minimal harness. 15+ providers incl. OpenRouter and Ollama. Extensions, skills, subagent extension. Free OSS, pay your own tokens.
- Buzz (Block / Jack Dorsey): https://buzz.xyz, https://github.com/block/buzz (Apache-2.0), launched 21 Jul 2026. Desktop app (Tauri+React) + CLI. A team workspace (Slack+GitHub-alike on a Nostr relay) where humans and agents are peers. Not a model harness itself: drives Claude Code, Codex, goose and any ACP agent. Free/self-hostable.
- herdr: https://herdr.dev, https://github.com/herdrdev/herdr. "Agent multiplexer that lives in your terminal." Rust single binary, Apache-2.0, 39.8k stars, Herdr, Inc. Shows every agent pane as working / blocked / idle, detach/reattach, SSH remote, socket API. Windows: `irm https://herdr.dev/install.ps1 | iex`.

## AI 3D generators
- Meshy https://www.meshy.ai: text/image→3D; GLB, FBX, OBJ, STL, 3MF, USDZ; PBR sets; auto-rig + animation clips.
- Tripo https://www.tripo3d.ai: STL/OBJ/FBX/GLB/GLTF/USD/USDZ/3MF; AI auto-rigging.
- Customuse https://customuse.com: AI 3D creation platform (web + mobile) for Roblox/Minecraft/avatar assets; prompt or image → mesh; engine-ready exports for Unity/Unreal/Roblox. Export formats and rigging unverified.
- Hyper3D Rodin https://hyper3d.ai: quad topology, T/A-pose, Blender/Unity/Unreal plugins. Alt: Tencent Hunyuan3D (free, self-hosted).

## Hosting
- Fly.io: usage-based, shared-cpu-1x 256MB from $2.02/mo, no free tier for new accounts. https://fly.io/docs/about/pricing/
- Websavers: founded 2004 in Halifax, Nova Scotia; Canadian shared/WordPress/VPS hosting on Canadian servers (Beauharnois, QC). https://websavers.ca/about

## ASD-STE100
https://www.asd-ste100.org/ "a controlled natural language and an international standard to write technical documentation."
