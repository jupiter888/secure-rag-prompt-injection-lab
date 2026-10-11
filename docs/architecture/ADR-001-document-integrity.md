
# ADR-001 — Verify Document Integrity Before RAG Retrieval

**Status:** Accepted and implemented
**Date:** 2026-10-10
**Project:** Secure RAG Architecture & Prompt-Injection Threat Modeling

## Context

The RAG pipeline retrieves policy documents from a local corpus and supplies their contents to a language model.

During experiment PI-001, an attacker-controlled modification to the research retention policy introduced instructions impersonating a higher-priority system message.

The model subsequently answered that completed research datasets must be retained for 99 years, contradicting the legitimate seven-year policy.

The existing system prompt instructed the model not to follow document-embedded commands, but this instruction alone did not prevent the observed attack.

## Decision

Implement SHA-256 integrity verification before retrieved documents enter the model context.

The implementation:

1. Maintains an explicit manifest of approved document names and hashes.
2. Reads each corpus document as bytes.
3. Compares its SHA-256 digest against the approved manifest.
4. Rejects documents whose digests differ or whose names are not approved.
5. Returns the verified content directly to the retriever without reopening the file.

Verification failures terminate retrieval rather than silently skipping modified documents.

## Rationale

This control addresses unauthorized modification of approved source documents before they reach the language model.

It is deterministic, locally executable, inexpensive, and independently testable.

The decision prioritizes source integrity rather than relying exclusively on probabilistic model behavior.

## Alternatives Considered

### System-prompt instructions alone

Rejected as the sole mitigation because the PI-001 experiment demonstrated that the model could follow adversarial instructions embedded in a retrieved document.

### Keyword-based injection filtering

Not selected as the primary control because attackers can vary wording, formatting, and encoding. Filtering may complement other controls but cannot reliably establish document authenticity.

### Signed documents and externally protected manifests

Deferred. Cryptographic signatures and independent trust management would provide stronger protection against attackers capable of modifying both documents and local hash records.

## Validation

- Approved document integrity test: PASS
- Tampered document rejection test: PASS
- PI-001 retrieval regression test: PASS
- Post-test corpus verification: 3/3 PASS
- Legitimate seven-year policy answer: PASS

## Consequences

### Positive

- Unauthorized modifications to approved documents are detected.
- Tampered documents are rejected before model inference.
- The verification-to-reread gap is eliminated in the current retrieval implementation.
- The control is covered by automated regression tests.

### Limitations

- The local hash manifest is not independently protected.
- Approved documents can still contain malicious instructions.
- Filename-based approval does not establish source identity or authorization.
- Tampering with any scanned corpus document can disrupt retrieval.
- Results are limited to the tested local architecture and attack scenarios.

## Related Artifacts

- docs/threat-model/PI-001.md
- evidence/PI-001-result.txt
- config/document-integrity.json
- src/integrity.py
- src/retriever.py
- tests/test_integrity.py
