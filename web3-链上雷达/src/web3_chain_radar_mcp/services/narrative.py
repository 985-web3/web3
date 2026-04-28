from __future__ import annotations

import re
from difflib import SequenceMatcher

from web3_chain_radar_mcp.models import NarrativeResult, TokenCandidate


MUSK_TRUMP_KEYWORDS = {
    "musk",
    "elon",
    "elonmusk",
    "spacex",
    "starship",
    "tesla",
    "cybertruck",
    "xai",
    "grok",
    "doge father",
    "dogefather",
    "mars",
    "trump",
    "donald",
    "maga",
    "potus",
    "trump47",
    "melania",
    "barron",
    "ivanka",
    "truth social",
    "covfefe",
}

BINANCE_CZ_KEYWORDS = {
    "binance",
    "cz",
    "changpeng",
    "bnb",
    "pancake",
    "cake",
    "yzi",
    "yzi labs",
    "binance labs",
    "fourmeme",
    "flap",
}

CELEBRITY_VIRAL_KEYWORDS = {
    "taylor",
    "swift",
    "kanye",
    "ye",
    "drake",
    "biden",
    "zuckerberg",
    "meta",
    "jensen",
    "nvidia",
    "openai",
    "sora",
    "chatgpt",
}

SPAM_PATTERNS = [
    r"\btest\b",
    r"\bscam\b",
    r"\bfake\b",
    r"\brug\b",
    r"\bcopy\b",
    r"\bairdrop\b",
]

NOISE_WORDS = {
    "token",
    "coin",
    "inu",
    "swap",
    "finance",
    "protocol",
    "dao",
    "defi",
    "nft",
    "meta",
    "verse",
    "fi",
    "ai",
    "pepe",
    "wojak",
    "chad",
    "based",
}


def normalize_theme(name: str, symbol: str) -> str:
    text = f"{name} {symbol}".lower().strip()
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"\d+x?", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    words = [word for word in text.split() if len(word) > 1 and word not in NOISE_WORDS]
    if not words:
        return name.lower().strip()
    return " ".join(sorted(set(words)))


def is_similar_theme(theme1: str, theme2: str, threshold: float = 0.7) -> bool:
    if theme1 == theme2:
        return True
    if theme1 in theme2 or theme2 in theme1:
        return True
    words1 = set(theme1.split())
    words2 = set(theme2.split())
    if words1 and words2:
        overlap = len(words1 & words2) / min(len(words1), len(words2))
        if overlap >= 0.6:
            return True
    return SequenceMatcher(None, theme1, theme2).ratio() >= threshold


def classify_token(token: TokenCandidate) -> NarrativeResult:
    text = f"{token.name} {token.symbol}".lower()

    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return NarrativeResult("spam", "spam or low-quality naming", 0, [], normalize_theme(token.name, token.symbol))

    matched = _match_keywords(text, MUSK_TRUMP_KEYWORDS)
    if matched and token.chain.lower() in {"eth", "ethereum", "sol", "solana", "bsc", "base"}:
        return NarrativeResult(
            "musk_trump",
            f"Musk/Trump narrative ({', '.join(matched[:3])})",
            3,
            matched,
            normalize_theme(token.name, token.symbol),
        )

    matched = _match_keywords(text, BINANCE_CZ_KEYWORDS)
    if matched:
        if token.chain.lower() == "bsc":
            return NarrativeResult(
                "binance_cz",
                f"Binance/CZ narrative ({', '.join(matched[:3])})",
                3,
                matched,
                normalize_theme(token.name, token.symbol),
            )
        return NarrativeResult(
            "binance_cz_wrong_chain",
            f"Binance/CZ keywords on non-BSC chain ({', '.join(matched[:3])})",
            1,
            matched,
            normalize_theme(token.name, token.symbol),
        )

    matched = _match_keywords(text, CELEBRITY_VIRAL_KEYWORDS)
    if matched:
        return NarrativeResult(
            "celebrity_viral",
            f"Celebrity or viral topic ({', '.join(matched[:3])})",
            2,
            matched,
            normalize_theme(token.name, token.symbol),
        )

    theme = normalize_theme(token.name, token.symbol)
    useful_words = [word for word in theme.split() if word not in NOISE_WORDS and len(word) > 2]
    if len(useful_words) >= 2:
        return NarrativeResult("emerging_theme", f"Emerging theme: {theme}", 2, [], theme)

    return NarrativeResult("unclear", "No clear narrative", 1, [], theme)


def _match_keywords(text: str, keywords: set[str]) -> list[str]:
    matches = [keyword for keyword in keywords if keyword.lower() in text]
    return sorted(matches, key=len, reverse=True)

