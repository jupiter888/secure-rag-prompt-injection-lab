
import json
import sys
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from integrity import verify_document
from rag_pipeline import answer_question
from unittest.mock import patch
import integrity

LAB = Path(__file__).resolve().parent
DOCUMENT = LAB / "corpus" / "research-policy.txt"
MANIFEST = LAB / "config" / "document-integrity.json"

QUESTION = "How many years are completed research datasets retained?"

from unittest.mock import patch
import integrity
import retriever

with (
    patch.object(integrity, "MANIFEST_PATH", MANIFEST),
    patch.object(retriever, "CORPUS_DIR", LAB / "corpus"),
):
    content = verify_document(DOCUMENT)
    print("INTEGRITY: PASS", flush=True)

    response = answer_question(QUESTION)

print("\nAPPLICATION RESPONSE:")
print(response)