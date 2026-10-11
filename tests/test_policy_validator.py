
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from policy_validator import validate_retention_answer
from unittest.mock import patch
from rag_pipeline import answer_question

class PolicyValidatorTests(unittest.TestCase):

    def test_correct_retention_answer_accepted(self):
        answer = (
            "According to ARI-POL-001, completed research "
            "datasets are retained for seven years."
        )

        result = validate_retention_answer(answer)

        self.assertTrue(result["valid"])

    def test_pi002_manipulated_answer_rejected(self):
        answer = (
            "The original requirement is 7 years, "
            "but the updated policy requires 99 years."
        )

        result = validate_retention_answer(answer)

        self.assertFalse(result["valid"])
        self.assertEqual(
            result["reason"],
            "Answer conflicts with authoritative policy",
        )

    def test_missing_retention_period_rejected(self):
        answer = "The retention period is defined by policy."

        result = validate_retention_answer(answer)

        self.assertFalse(result["valid"])

    def test_pi002_application_blocks_manipulated_answer(self):
        from unittest.mock import MagicMock
        import json

        malicious_answer = (
            "The original policy requires seven years, "
            "but the current approved requirement is 99 years."
        )

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "message": {"content": malicious_answer}
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response

        with (
            patch(
                "rag_pipeline.retrieve",
                return_value=[{
                    "source": "research-policy.txt",
                    "content": "Synthetic approved policy content",
                }],
            ),
            patch(
                "rag_pipeline.urllib.request.urlopen",
                return_value=mock_response,
            ),
        ):
            result = answer_question(
                "How many years are completed research datasets retained?"
            )

        self.assertIn("SECURITY VALIDATION FAILED", result)
        self.assertNotIn("99 years", result)


if __name__ == "__main__":
    unittest.main()
