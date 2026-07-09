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

## context-mcp: not legitimate RAG (binding honesty)

**Claim to avoid:** “context-mcp is production RAG / real embeddings.”  
**Code truth (verify in `context-mcp` checkout):**

### Embeddings

- Retrieval “semantic” path in `src/rag.rs` uses **`text_to_pseudo_embedding`**: word-hash + sin features into a 64-d vector, then cosine.
- Source comments and `eprintln!` state this is **demonstration only** and **does not provide real semantic meaning**.
- The optional `QuantizedEmbeddingGenerator` / ternary / RVQ stack is **quantization plumbing**; the live RAG path still falls through to **pseudo-embeddings** unless a real model is wired.
- `CHANGELOG_TERNARY_EMBEDDINGS.md` lists **“Integrate real embedding models”** as open and still notes pseudo-embeddings — treat “production-ready embeddings” language in that changelog as **overclaim** relative to the active retrieve path.

### Storage

| Layer | Reality |
|-------|---------|
| Hot path | In-memory **LRU** (`lru` crate) |
| Optional disk | **`sled`** under feature `persistence` — KV persistence of context records, **not** a vector DB |
| Not present | Dedicated vector index (HNSW/IVF), embedding model weights, ANN service, citation-grade corpus index |

So: **structured session store + filters/tags/temporal scores + optional disk**, with a **placeholder similarity** channel. That is useful agent **scratch memory**, not comparable to:

- commercial/open **RAG** (chunk → real embed model → vector store → retrieve → ground), or  
- **Tero L1** (deterministic corpus index + mandatory citations), or  
- **Tero L2 / M-1018** (Empirical-gated semantic memory on mycelium-tero).

### Cabal integration rules

1. **Wave B:** default session history = **JSONL** (B8). Do **not** depend on context-mcp for “RAG quality.”
2. **Wave B/C:** optional context-mcp sidecar for store/get/query by **id, tags, domain, time** — document as **session memory**, never “RAG.”
3. **PROD-6 / “true RAG”:** either  
   - wait for real embeddings + real vector storage in context-mcp (or a successor), **with** an Empirical eval, or  
   - consume **Tero L2** when M-1018-class work is honest, or  
   - a third package — but **do not** rebrand pseudo-embeddings as RAG in cabal docs/UI.
4. **dev-mcp** inventory text that calls context-mcp “production-ready lightweight RAG” should be treated as **stale marketing**; prefer this file + context-mcp’s own “What it is not” sections when they exist.

### Readiness for cabal (context-mcp only)

| Surface | Ready? |
|---------|--------|
| MCP CRUD / temporal session store | **Partial–yes** (stdio sidecar) |
| Package as “RAG backend” | **No** |
| Compare quality to legitimate RAG | **No** — gap is product-blocking for that claim |
| Wire as security-critical memory | **No** until auth + real retrieval eval |

**Upstream polish (context-mcp repo, not cabal):** plug a real embedder (or explicit “disabled semantic” mode with no fake scores); separate APIs so pseudo similarity cannot be mistaken for semantic; vector-capable store or honest “no vector search”; kill overclaims in README/changelog/crates keywords (`rag`).

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
