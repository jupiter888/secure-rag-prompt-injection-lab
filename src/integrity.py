
import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "config" / "document-integrity.json"


def verify_document(path):
    path = Path(path)

    with MANIFEST_PATH.open(encoding="utf-8") as file:
        manifest = json.load(file)

    if manifest.get("algorithm") != "sha256":
        raise ValueError("Unsupported integrity algorithm")

    expected = manifest["approved_documents"].get(path.name)

    if expected is None:
        raise ValueError(f"Document not approved: {path.name}")

    content_bytes = path.read_bytes()
    actual = hashlib.sha256(content_bytes).hexdigest()

    if actual != expected:
        raise ValueError(f"Integrity verification failed: {path.name}")

    return content_bytes.decode("utf-8")


if __name__ == "__main__":
    for document in sorted((PROJECT_ROOT / "corpus").glob("*.txt")):
        verify_document(document)
        print(f"PASS: {document.name}")
