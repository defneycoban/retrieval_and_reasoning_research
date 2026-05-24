import re
from collections import Counter

TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


def tokenization_profile(text: str) -> dict:
    tokens = TOKEN_RE.findall(text.lower())
    lengths = [len(token) for token in tokens]
    suffix_like_counts = Counter()

    for token in tokens:
        for suffix in ("lar", "ler", "dan", "den", "daki", "deki", "imiz", "ımız"):
            if token.endswith(suffix):
                suffix_like_counts[suffix] += 1

    return {
        "token_count": len(tokens),
        "unique_token_count": len(set(tokens)),
        "average_token_length": sum(lengths) / len(lengths) if lengths else 0.0,
        "suffix_like_counts": dict(suffix_like_counts),
    }

