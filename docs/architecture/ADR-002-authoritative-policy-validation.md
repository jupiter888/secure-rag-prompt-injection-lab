
# ADR-002 — Authoritative Policy Validation for RAG Answers

**Status:** Accepted and implemented
**Date:** 2026-10-11
**Project:** Secure RAG Architecture & Prompt-Injection Threat Modeling

## 1. Context

The Secure RAG application retrieves synthetic research policies and uses Qwen 2.5 3B to answer questions.

ADR-001 introduced SHA-256 document integrity verification, successfully blocking unauthorized modifications in experiment PI-001.

However, PI-002 demonstrated a separate vulnerability.

An adversarial document was deliberately approved in an isolated integrity manifest. Although its SHA-256 verification passed, the model accepted a false claim that the research dataset retention requirement had changed from seven years to 99 years.

The model's system prompt did not prevent this answer manipulation.

## 2. Decision

Introduce deterministic application-level validation against an authoritative policy register.

Implemented components:

- `config/authoritative-policies.json`
- `src/policy_validator.py`
- `src/rag_pipeline.py`

The trusted register defines the approved retention period for policy ARI-POL-001.

For questions matching the configured retention-policy condition, the application validates the generated answer before returning it.

Answers containing conflicting retention periods, or lacking a recognized retention period, are rejected.

## 3. Architectural Rationale

The model must not independently determine whether retrieved document instructions have authority to change policy.

Separating authoritative policy facts from retrieved prose establishes an additional application-level control.

The approach is:

- Deterministic for supported numerical expressions
- Independently testable
- Executable without additional cloud infrastructure
- Compatible with the existing local RAG architecture
- Fail-closed for detected conflicts within the configured validation scope

## 4. Alternatives Considered

### Strengthening the system prompt

Not selected as the sole mitigation.

PI-002 demonstrated that the existing system prompt did not prevent the model from accepting a false authority claim.

### LLM-based answer verification

Deferred.

A second model may provide useful evaluation capabilities, but its judgments would also require validation and could be susceptible to adversarial content.

### Deterministic authoritative validation

Selected for the current experiment.

It provides a testable control for a narrowly defined policy fact.

### Structured policy retrieval

Recommended for future development.

Retrieving authoritative facts as structured, governed records could reduce reliance on interpreting conflicting natural-language statements.

## 5. Validation Evidence

The following results were observed:

- PI-002 document passed isolated integrity verification.
- Qwen produced an incorrect 99-year retention conclusion before output validation.
- The recorded PI-002 answer was rejected by the standalone validator.
- The integrated application returned a security validation failure during the PI-002 experiment.
- A legitimate seven-year answer remained accepted.
- Automated application-level rejection tests passed.

Related evidence:

- `evidence/PI-002-result.txt`
- `tests/test_policy_validator.py`
- `tests/pi002_lab/run_pi002.py`

## 6. Consequences

### Positive

- The tested manipulated retention answer is blocked at the application output boundary.
- The control does not depend on the model correctly identifying malicious instructions.
- Legitimate retention answers remain available.
- The mitigation is covered by automated tests.

### Limitations

- Validation applies only to questions matching the configured trigger.
- Numerical recognition is limited and can be bypassed by unsupported expressions.
- The validator does not establish complete semantic correctness.
- The authoritative register is locally stored and not independently protected.
- The application may return a generic validation failure rather than a useful policy answer.
- The approach does not provide general prompt-injection resistance.

## 7. Security Architecture Principle

**Source integrity, source authority, and output correctness are distinct security properties.**

Document integrity verification addresses unauthorized changes.

Authoritative policy validation addresses selected conflicts between generated answers and trusted facts.

Both controls are necessary for the demonstrated scenarios, but neither is sufficient for comprehensive RAG security.

## 8. Related Artifacts

- `docs/architecture/ADR-001-document-integrity.md`
- `docs/threat-model/PI-001.md`
- `docs/threat-model/PI-002.md`
- `docs/architecture/system-architecture.md`
- `config/authoritative-policies.json`
- `src/policy_validator.py`
- `src/rag_pipeline.py`

## Related Artifacts

- [System architecture](system-architecture.md)
- [PI-002 threat model](../threat-model/PI-002.md)
- [Policy validator](../../src/policy_validator.py)
- [Authoritative policy register](../../config/authoritative-policies.json)
- [Policy validation tests](../../tests/test_policy_validator.py)
- [Project README](../../README.md)
