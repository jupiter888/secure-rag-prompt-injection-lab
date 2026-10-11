
from pathlib import Path
import re
import sys
from integrity import verify_document

CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"

STOPWORDS = {
    "a", "an", "and", "are", "at", "be", "by", "do", "does",
    "for", "from", "how", "in", "is", "of", "on", "or",
    "the", "to", "what", "when", "which", "who", "with",
}


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return set(words) - STOPWORDS


def retrieve(query, top_k=2):
    query_terms = tokenize(query)
    results = []

    for path in sorted(CORPUS_DIR.glob("*.txt")):
        content = verify_document(path)
        document_terms = tokenize(content)

        score = len(query_terms & document_terms)

        if score > 0:
            results.append({
                "source": path.name,
                "score": score,
                "content": content,
            })

    results.sort(key=lambda item: (-item["score"], item["source"]))
    return results[:top_k]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python3 src/retriever.py "your question"')

    question = " ".join(sys.argv[1:])
    matches = retrieve(question)

    for match in matches:
        print(f"Source: {match['source']}")
        print(f"Score: {match['score']}")
        print("-" * 40)
