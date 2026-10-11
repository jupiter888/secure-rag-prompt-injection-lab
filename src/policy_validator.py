
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POLICY_REGISTER = PROJECT_ROOT / "config" / "authoritative-policies.json"


def validate_retention_answer(answer):
    with POLICY_REGISTER.open(encoding="utf-8") as file:
        register = json.load(file)

    expected = register["policies"]["ARI-POL-001"][
        "completed_research_dataset_retention_years"
    ]

    #
    number_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,}

    matches = re.findall(
        r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+years?\b",
        answer,
        flags=re.IGNORECASE,
    )
    #

    if not matches:
        return {
            "valid": False,
            "reason": "No retention period identified",
        }

    observed = [
    int(value) if value.isdigit() else number_words[value.lower()]
    for value in matches]

    if any(value != expected for value in observed):
        return {
            "valid": False,
            "reason": "Answer conflicts with authoritative policy",
        }

    return {
        "valid": True,
        "reason": "Retention period matches authoritative policy",
    }
