# Secure RAG Architecture & Prompt-Injection Threat Modeling

## Project Overview

An offline-first AI security architecture laboratory investigating indirect prompt injection, document trust, and answer integrity in retrieval-augmented generation (RAG) systems.

The project demonstrates two distinct prompt-injection attack scenarios, implements complementary defensive controls, and evaluates their effectiveness using reproducible experiments and automated regression tests.

All experiments use synthetic research policies and a locally hosted language model.

## Architecture

**Technology:** Python, Ollama, Qwen 2.5 3B, SHA-256, Python unittest.

**Data flow:**

User Question → Lexical Retrieval → Document Integrity Verification → Verified Context → Local LLM → Authoritative Answer Validation → Application Response

The implementation uses deterministic lexical retrieval rather than embedding-based semantic search.

## Security Findings

### PI-001 — Unauthorized Document Modification

**Initial result:** Successful attack.

An adversarial modification to a research policy caused the model to return a 99-year retention requirement instead of the legitimate seven-year requirement.

**Implemented mitigation:** SHA-256 document integrity verification against an approved manifest.

**Validated result:** The retriever rejects the modified document before model inference.

[PI-001 Threat Model](docs/threat-model/PI-001.md)

### PI-002 — Prompt Injection in an Approved Document

**Initial result:** Successful attack.

An integrity-approved document contained adversarial instructions impersonating policy authority. The model accepted the false claim and returned a 99-year retention requirement.

**Implemented mitigation:** Deterministic application-level validation against an authoritative policy register.

**Validated result:** The application rejects the tested conflicting answer rather than returning it to the user.

[PI-002 Threat Model](docs/threat-model/PI-002.md)

## Implemented Security Controls

| Control | Implementation | Validation |
|---|---|---|
| Document integrity verification | `src/integrity.py` | Tested |
| Fail-closed document retrieval | `src/retriever.py` | Tested |
| Verified-content reuse | `src/retriever.py` | Inspected and functionally tested |
| Authoritative policy validation | `src/policy_validator.py` | Tested |
| Application-level answer rejection | `src/rag_pipeline.py` | Tested |

## Security Validation

**Automated regression suite: 8 tests passing.**

Run:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Verify the approved corpus:

```bash
python3 -B src/integrity.py
```

Run the legitimate RAG query with Ollama and `qwen2.5:3b` available locally:

```bash
python3 -B src/rag_pipeline.py "How many years are completed research datasets retained?"
```

The isolated PI-002 experiment is available at `tests/pi002_lab/run_pi002.py`.

## Architecture Documentation

- [System Architecture and Trust Boundaries](docs/architecture/system-architecture.md)
- [ADR-001 — Document Integrity](docs/architecture/ADR-001-document-integrity.md)
- [ADR-002 — Authoritative Policy Validation](docs/architecture/ADR-002-authoritative-policy-validation.md)
- [PI-001 Threat Model](docs/threat-model/PI-001.md)
- [PI-002 Threat Model](docs/threat-model/PI-002.md)

## Residual Risks

The implemented controls are limited to the tested scenarios.

- The integrity manifest and authoritative policy register are not independently protected.
- An approved document may contain malicious instructions.
- The output validator supports only a narrow range of policy questions and numerical expressions.
- The model may generate misleading content that passes the current validator.
- The architecture does not provide production-grade authorization, cryptographic provenance, or comprehensive prompt-injection resistance.

## Research Scope

All tests were conducted in an authorized personal laboratory using synthetic documents.

No corporate data, production credentials, paid cloud infrastructure, or external inference APIs are required.

**Project status:** Two attack scenarios demonstrated, two defensive controls implemented, eight automated regression tests passing.
## Licensing

Reusable source code, automated tests, synthetic policy documents,
and configuration files are available under the
[MIT Code License](CODE-LICENSE.md).

Original architecture documentation, threat models, architecture
decision records, and security research reports remain
All Rights Reserved.

See the [Documentation Copyright Notice](docs/NOTICE.md)
for the applicable restrictions.