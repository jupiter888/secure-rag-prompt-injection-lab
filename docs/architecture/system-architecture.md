
# Secure RAG — System Architecture and Trust Boundaries

## 1. Architecture Overview

This project implements a local Retrieval-Augmented Generation (RAG) pipeline using Python and Ollama with the Qwen 2.5 3B language model.

The application answers questions about synthetic research policies.

All policy documents are synthetic. No production systems, credentials, or confidential organizational data are required.

## 2. Data Flow

User Question
    |
    v
RAG Pipeline
    |
    v
Lexical Retriever
    |
    v
Local Document Corpus
    |
    v
SHA-256 Integrity Verification
    |
    v
Verified Document Content
    |
    v
Context Assembly + System Prompt
    |
    v
Local Ollama API / Qwen 2.5 3B
    |
    v
Generated Answer
    |
    v
Authoritative Policy Validator
    |                    |
    | Valid              | Invalid
    v                    v
Return Answer       Return Security
                    Validation Failure

The diagram represents the logical flow. During retrieval, the application reads each scanned corpus document and verifies its content before using it.

## 3. System Components

### User Interface

Command-line interface accepting a natural-language question.

### Retrieval Layer

Deterministic lexical retrieval that scores documents by shared query terms.

Current implementation selects the highest-ranked matching document for the RAG pipeline.

### Document Corpus

Three synthetic policy documents:

- ARI-POL-001: Research Data Retention
- ARI-SEC-002: Access Control
- ARI-IR-003: Incident Response

### Integrity Control

SHA-256 verification against an approved document manifest.

Documents failing verification are rejected before their contents enter the model context.

### Model Inference

Ollama provides a local API at 127.0.0.1:11434.

The configured model is qwen2.5:3b.

## 4. Trust Boundaries

### TB-01: User Input to Application

User questions enter the application as untrusted input.

Risk: Malicious instructions or unexpected input affecting retrieval or model behavior.

Current controls: Local execution and fixed application logic.

### TB-02: Document Corpus to Retrieval Layer

Policy documents represent lower-trust content.

Risk: Unauthorized modifications and embedded adversarial instructions.

Implemented control: SHA-256 document integrity verification.

Residual risk: The approved hash manifest is not independently protected.

### TB-03: Retrieved Content to LLM Context

Verified document text enters the model's context.

Risk: The model may interpret document-embedded instructions as authoritative commands.

Current controls: System-prompt instructions and document delimiters.

Residual risk: These measures do not guarantee instruction/data separation.

### TB-04: Application to Local Model Service

The application sends prompts to Ollama over a local HTTP endpoint.

Risk: Unauthorized local access, service misconfiguration, or unintended network exposure.

Current scope: Local laboratory environment.

No production authentication, transport-security, or service-isolation guarantees have been validated.

### TB-05: Model Output to User

Generated answers cross the application output boundary
before being presented to the user.

Risk: Prompt-injection-induced answer manipulation,
incorrect policy values, or unsupported claims.

Implemented control:
- Deterministic validation against the authoritative
  policy register for supported retention-policy questions.
- Rejection of answers containing conflicting or missing
  recognized retention periods.

Evidence:
- PI-002 demonstrated successful answer manipulation
  before output validation.
- Integrated output validation rejected the tested
  manipulated response.
- Legitimate seven-year answers remained accepted.

Residual risks:
- Validation covers only configured question patterns.
- Unsupported numerical expressions may bypass detection.
- Correct numerical values do not guarantee overall
  answer correctness.
- The authoritative register is not independently protected.

## 5. Security Objectives

- Preserve the integrity of approved policy documents.
- Prevent unauthorized corpus modifications from influencing model answers.
- Maintain correct behavior for legitimate queries.
- Identify and document remaining prompt-injection risks.
- Provide reproducible evidence for security architecture decisions.

## 6. Scope and Limitations

This is a local, synthetic security research laboratory.

The project does not claim production-grade document authorization, cryptographic provenance, comprehensive prompt-injection resistance, or independently verified answer correctness.

## 7. Related Artifacts

### Threat Models and Evidence
- [PI-001 — Unauthorized Document Modification](../threat-model/PI-001.md)
- [PI-001 — Recorded Attack Evidence](../../evidence/PI-001-result.txt)
- [PI-002 — Approved Adversarial Document](../threat-model/PI-002.md)
- [PI-002 — Recorded Attack Evidence](../../evidence/PI-002-result.txt)

### Architecture Decisions
- [ADR-001 — Document Integrity](ADR-001-document-integrity.md)
- [ADR-002 — Authoritative Policy Validation](ADR-002-authoritative-policy-validation.md)

### Trusted Configuration and Corpus
- [Document Integrity Manifest](../../config/document-integrity.json)
- [Authoritative Policy Register](../../config/authoritative-policies.json)
- [Synthetic Research Policy](../../corpus/research-policy.txt)

### Implementation and Tests
- [Document Retriever](../../src/retriever.py)
- [Document Integrity Verification](../../src/integrity.py)
- [RAG Pipeline](../../src/rag_pipeline.py)
- [Policy Validator](../../src/policy_validator.py)
- [Document Integrity Tests](../../tests/test_integrity.py)
- [Policy Validation Tests](../../tests/test_policy_validator.py)
- [PI-002 Isolated Experiment](../../tests/pi002_lab/run_pi002.py)

[Return to project README](../../README.md)
