# Agentic Content Pipeline – Development Roadmap

This roadmap outlines the phased development of a modular, agentic content generation pipeline. Each agent is built, tested, and API-integrated independently. The system will support flexible LLM configuration per agent and a creative vs grounded content mode.

## 📌 Core Goals

* Human-like, insightful, multi-format content (threads, essays, commentary)
* Grounded or creative content generation (user-controlled)
* Modular agents with independent prompts, LLMs, and responsibilities
* Reusable shared infrastructure (logging, DB access, LLM clients, etc.)

---

## 🔁 Phase 0: Foundations (Already Refactored)

* ✅ Modular folder structure per agent (`app/agents/{agent_name}/`)
* ✅ Shared utils for logging, LLM clients, retry logic
* ✅ Centralised config file + `.env`

---

## 🌱 Phase 1: Content Planner Agent (self-directed)

* **Purpose**: Takes raw topic and determines content intent, angle, and research/composition plan
* **Output**: `framed_topic`, `content_type`, `content_angle`, `structure_plan`
* **Config**:

  * Per-agent LLM config (`gpt-4`, `claude`, etc.)
  * Prompt file
* **API**: `POST /agents/content-planner/run`
* **Tests**:

  * Input topic ➝ plan structure JSON
  * Error cases (empty topic, invalid input)

---

## 📚 Phase 2: Grounding Agent

* **Purpose**: For each planned content element, fetch real-world source or flag as fictional
* **Sources**:

  * Google Search (articles, blogs)
  * ArXiv (optional)
  * Tweets or public posts
* **Schema**: Updates `research_sources` table
* **API**: `POST /agents/grounding/run`
* **Tests**:

  * Fetch source ➝ validate accessibility
  * Score freshness/relevance

---

## 🧠 Phase 3: Content Composer Agent

* **Purpose**: Takes structured plan and sources to generate full content (thread/article)
* **Honours**: Tone, persona, format, voice
* **Input**: `structure_plan`, verified sources
* **Output**: Formatted draft
* **API**: `POST /agents/content-composer/run`
* **Tests**:

  * Compose valid content
  * Check word count, flow

---

## 🧪 Phase 4: Critic Agent (optional, scoring/rewrites)

* **Purpose**: Evaluate or compare multiple drafts (if generated)
* **Output**: Ranked versions or suggested rewrite prompts
* **API**: `POST /agents/critic/run`
* **Tests**:

  * Score quality/coherence
  * Validate structure compliance

---

## 🧷 Phase 5: Integration Layer

* Hook each agent via API
* Manage lifecycle per `request_id`
* Persist outputs and intermediate steps
* Add final route: `POST /content/requests/full-pipeline`

---

## 🛠 Shared Services Checklist

* [ ] `utils/llm_clients.py` – Wrapper classes for OpenAI, Anthropic, etc.
* [ ] `utils/prompts.py` – Prompt file loader
* [ ] `services/db.py` – Helper functions for research/source DB ops
* [ ] `utils/logging.py` – Structured logger
* [ ] `schemas/` – Pydantic models for request/response payloads

---

## 🧪 Testing Strategy

* Unit tests for each agent
* API integration tests
* Scenario tests (creative vs grounded mode)
* Mock LLM responses for test reliability

---

## 🗃 Example Directory Layout (per agent)

```
app/
├── agents/
│   ├── content_planner_agent/
│   │   ├── agent.py
│   │   ├── prompts/
│   │   │   └── planner_prompt.txt
│   │   ├── llm_config.py
│   │   └── schema.py
```

---

Let this file evolve as we build. ✅ = Completed | 🔄 = In Progress | ⏳ = Upcoming

✅ What We've Built & Verified
| Feature                                          | Status |
| ------------------------------------------------ | ------ |
| Prompt template (flexible, escaped)              | ✅      |
| Schema (`Input`, `Output`, `Section`)            | ✅      |
| Modular agent with `run()` method                | ✅      |
| LLM engine with per-agent configuration          | ✅      |
| Robust LLM response parsing & recovery           | ✅      |
| Working `FakeLLM` for testing                    | ✅      |
| Test harness (`test.py`)                         | ✅      |
| FastAPI endpoint (`/agents/content-planner/run`) | ✅      |
| Unit tests via Pytest (success + failure)        | ✅      |

✅ Bonus Improvements (Optional Later)
| Enhancement                       | Worth Doing Later? |
| --------------------------------- | ------------------ |
| Log to file or DB for debugging   | 🔄 optional        |
| Add caching for repeated prompts  | 🔄 optional        |
| Add OpenAPI docs example response | 🔄 optional        |
| Log execution time per request    | 🔄 optional        |
