# Local sibling tooling (MCP / packages)

**Status:** Living notes (2026-07-08)  
**Layout:** siblings under the same git parent as this repo (e.g. `/root/git` or `~/git`).  
**Investigation rule:** excavate with **Tero first** ([AGENTS.md](../AGENTS.md)), then verify code in each checkout.

This document records **honest readiness** for wiring siblings into cabal-devmelopner as MCP servers and/or packages. It is not a substitute for each repo’s own README.

---

## Inventory (typical parent dir)

| Repo | Role | Cabal wave |
|------|------|------------|
| `tero-mcp` | Corpus L1 cited memory MCP | PoC+ (already wired) |
| `mycelium` | Default Tero index + full `mycelium-tero` later | Index now; L2 later |
| `context-mcp` | **Session** memory MCP (not corpus RAG) | B/C optional — **see RAG gap below** |
| `security-mcp` | Text screening MCP | D (hooks earlier) |
| `agent-mcp` | Multi-provider orchestration MCP | D optional |
| `webpuppet-rs` / `webpuppet-rs-mcp` | Browser automation | D, never default-on |
| `search-box` | Search MCP | After `develop` → usable main |
| `dev-mcp` | Docs umbrella only | Orientation |

---

## context-mcp: not legitimate RAG yet — and **must become** efficient legitimate RAG

**Product need (maintainer):** context-mcp **requires** efficient, **legitimate** RAG — not pseudo-similarity theater. That is an **upstream requirement** on the `context-mcp` repo before cabal (or any agent) may treat it as a RAG backend.

**Claim to avoid today:** “context-mcp is production RAG / real embeddings.”  
**Code truth today (verify in `context-mcp` checkout):**

### Embeddings (gap)

- Retrieval “semantic” path in `src/rag.rs` uses **`text_to_pseudo_embedding`**: word-hash + sin features into a 64-d vector, then cosine.
- Source comments and `eprintln!` state this is **demonstration only** and **does not provide real semantic meaning**.
- The optional `QuantizedEmbeddingGenerator` / ternary / RVQ stack is **quantization / efficiency plumbing** — valuable *after* real vectors exist; it does **not** replace a real embedder.
- `CHANGELOG_TERNARY_EMBEDDINGS.md` lists **“Integrate real embedding models”** as open — treat “production-ready embeddings” language as **overclaim** relative to the active retrieve path.

### Storage (gap)

| Layer | Reality today |
|-------|----------------|
| Hot path | In-memory **LRU** (`lru` crate) |
| Optional disk | **`sled`** under feature `persistence` — KV of context records, **not** a vector index |
| Not present | Real embed model I/O, ANN/HNSW (or equivalent), durable embedding cache, retrieval eval harness |

So today: **structured session store + filters/tags/temporal scores + optional disk**, with a **placeholder similarity** channel. Useful agent **scratch memory**, **not** legitimate RAG.

### Definition of “efficient legitimate RAG” (exit for this gap)

Upstream context-mcp is **RAG-ready** only when **all** of the following hold:

1. **Real embeddings** — pluggable embedder (local and/or API) producing dense (or agreed sparse) vectors with documented dims/model id; **no silent fallback** to hash pseudo-vectors when semantic mode is on (fail closed or explicit `semantic=off`).
2. **Real vector storage / retrieval** — index suited to scale (ANN or honest exact search with documented limits); embeddings persisted with items; rebuild/reindex story.
3. **Efficiency** — batch embed, cache-by-content-hash, quantized path *optional and measured* (ternary/RVQ may land here **after** baseline dense is correct); p95 latency budgets documented for local use.
4. **Retrieval API honesty** — tools/scores distinguish keyword/metadata rank vs semantic rank; never label pseudo scores as “semantic.”
5. **Empirical gate** — small eval set (questions → expected context ids) with precision/recall or nDCG vs keyword baseline; **no “improved RAG” claim without numbers** (same honesty posture as DN-87 / Tero L2).
6. **Secure local defaults** — stdio or loopback; no unauthenticated public bind; no secrets in stored contexts by default.

Until then, context-mcp remains **session memory MCP**, not RAG.

### Split of roles (do not collapse)

| System | Role |
|--------|------|
| **Tero L1** | Cited **corpus** memory (docs/decisions/issues) |
| **Tero L2** (future) | Corpus semantic layer (Empirical-gated) |
| **context-mcp (today)** | **Session / run** scratch store |
| **context-mcp (required future)** | Efficient **legitimate RAG** over agent/session (and optionally project) context **plus** honest session KV |

Cabal may use **both**: Tero for project truth, context-mcp for runtime/session RAG **after** the exit criteria above.

### Cabal integration rules

1. **Wave B:** default session history = **JSONL** (B8). Do **not** depend on context-mcp for “RAG quality.”
2. **Wave B/C:** optional context-mcp sidecar for store/get/query by **id, tags, domain, time** — document as **session memory**, never “RAG.”
3. **PROD-6 / “true RAG” via context-mcp:** blocked on upstream meeting **Definition of efficient legitimate RAG** above. Alternatives: Tero L2 when honest, or another package — **never** rebrand pseudo-embeddings as RAG in cabal docs/UI.
4. **dev-mcp** “production-ready lightweight RAG” for context-mcp = **stale**; fix upstream inventory when refreshing dev-mcp.

### Readiness for cabal (context-mcp only)

| Surface | Ready? |
|---------|--------|
| MCP CRUD / temporal session store | **Partial–yes** (stdio sidecar) |
| Package as “RAG backend” | **No** — **required future**, not optional nicety |
| Compare quality to legitimate RAG | **No** — product-blocking gap |
| Wire as security-critical memory | **No** until auth + real retrieval eval |

### Upstream work (context-mcp repo — track there)

Suggested issue themes (file on `tzervas/context-mcp`):

1. `[P0] Real embedder interface + kill silent pseudo-embedding in semantic mode`  
2. `[P0] Vector store / ANN (or bounded exact) + persist embeddings with items`  
3. `[P1] Content-hash embed cache + batch embed`  
4. `[P1] Retrieval eval harness (baseline vs semantic)`  
5. `[P2] Quantization path (ternary/RVQ) as efficiency layer on real vectors only`  
6. `[P2] Docs: remove RAG overclaims until eval passes`  

Cabal tracks consumption only: [OPEN_ISSUES.md](OPEN_ISSUES.md) MVP-7 / PROD-6; [ROADMAP.md](ROADMAP.md) D6b.

---

## Other siblings (one-liners)

| Repo | Honest note |
|------|-------------|
| **tero-mcp** | Real L1 MCP; not L2; not index builder |
| **security-mcp** | Heuristic text screener; not supply-chain scanner; proxy branch unfinished |
| **agent-mcp** | Alpha; browser/webpuppet-oriented multi-prompt, not cabal’s API Provider ABC |
| **webpuppet-*** | High risk; security pairing incomplete; Wave D only |
| **search-box** | Real work on `develop`, scaffold on `main` |

Branch/in-flight detail from the 2026-07-08 audit lives in session notes (`/tmp/investigate-*.md`); re-run with **Tero-first** leaf prompts when refreshing.

---

## Related

- [ROADMAP.md](ROADMAP.md) — waves and PR plan  
- [TERO.md](TERO.md) — Tero L1 vs everything else  
- [AGENTS.md](../AGENTS.md) — subagent Tero excavation checklist  
- DN-87 honesty: never claim improved-on-RAG without Empirical measurement (mycelium corpus)
