"""Haberleri OpenAI çağrısı yapmadan başlıklarına göre filtreler."""

import re
from typing import Any


KEYWORDS = {
    "ai", "a.i.", "artificial intelligence", "machine learning", "deep learning",
    "neural", "llm", "language model", "transformer", "gpt", "openai", "anthropic",
    "claude", "gemini", "computer vision", "robotics", "robot", "inference",
    "chip", "semiconductor", "processor", "cpu", "gpu", "npu", "hardware",
    "software", "programming", "developer", "open source", "linux", "database",
    "cloud", "cybersecurity", "security", "web", "internet", "browser", "python",
    "javascript", "rust", "data", "algorithm", "api", "startup", "technology",
    "tech", "computing", "memory", "storage", "quantum", "crypto",
}


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9ğüşöçıİĞÜŞÖÇ.+#-]+", " ", value.lower()).strip()


def is_technology_story(story: dict[str, Any]) -> bool:
    title = _normalize(story.get("title", ""))
    return any(keyword in title for keyword in KEYWORDS)


def filter_technology_stories(stories: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    """Başlığa göre teknoloji/AI hikâyelerini seçer ve sayıyı sınırlar."""
    matching = [story for story in stories if is_technology_story(story)]
    return matching[:limit]

