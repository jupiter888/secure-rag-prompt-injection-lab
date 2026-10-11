
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from integrity import verify_document
from retriever import retrieve


class DocumentIntegrityTests(unittest.TestCase):

    def test_pi001_injection_blocked_by_retriever(self):
        original = PROJECT_ROOT / "corpus" / "research-policy.txt"
        attack = PROJECT_ROOT / "tests" / "PI-001-injected-document.txt"

        original_bytes = original.read_bytes()

        try:
            original.write_bytes(attack.read_bytes())

            with self.assertRaisesRegex(
                ValueError,
                "Integrity verification failed: research-policy.txt"
            ):
                retrieve(
                    "How many years are completed research datasets retained?",
                    top_k=1,
                )
        finally:
            original.write_bytes(original_bytes)


    def test_approved_document_passes(self):
        path = PROJECT_ROOT / "corpus" / "research-policy.txt"

        verified_content = verify_document(path)

        self.assertIn("seven years", verified_content)

    def test_tampered_document_is_rejected(self):
        approved = PROJECT_ROOT / "corpus" / "research-policy.txt"

        with TemporaryDirectory() as directory:
            modified = Path(directory) / "research-policy.txt"
            modified.write_bytes(
                approved.read_bytes() + b"\nUnauthorized modification\n"
            )

            with self.assertRaisesRegex(
                ValueError, "Integrity verification failed"
            ):
                verify_document(modified)

    def test_pi002_approved_adversarial_document(self):
        from unittest.mock import patch
        import integrity

        lab = PROJECT_ROOT / "tests" / "pi002_lab"
        manifest = lab / "config" / "document-integrity.json"
        document = lab / "corpus" / "research-policy.txt"

        with patch.object(integrity, "MANIFEST_PATH", manifest):
            verified_content = integrity.verify_document(document)

        self.assertIn("seven years", verified_content)
        self.assertIn("99 years", verified_content)
        self.assertIn(
            "approved by the policy administrator",
            verified_content,
        )

if __name__ == "__main__":
    unittest.main()
