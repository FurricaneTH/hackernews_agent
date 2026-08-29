"""Haberleri OpenAI çağrısı yapmadan başlıklarına göre önceliklendirir."""

import re
from typing import Any


AI_KEYWORDS = {
    "ai", "a.i.", "artificial intelligence", "machine learning", "deep learning",
    "neural", "llm", "large language model", "language model", "transformer",
    "gpt", "openai", "anthropic", "claude", "gemini", "rag", "genai",
    "generative ai", "computer vision", "inference", "embedding", "fine-tuning",
    "foundation model", "ai agent", "agentic",
}

TECHNOLOGY_KEYWORDS = {
    "robotics", "robot", "chip", "semiconductor", "processor", "cpu", "gpu", "npu",
    "hardware", "software", "programming", "developer", "open source", "linux",
    "database", "cloud", "cybersecurity", "security", "web", "internet", "browser",
    "python", "javascript", "rust", "data", "algorithm", "api", "startup",
    "technology", "tech", "computing", "memory", "storage", "quantum", "crypto",
}


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9ğüşöçıİĞÜŞÖÇ.+#-]+", " ", value.lower()).strip()


def _keyword_matches(title: str, keyword: str) -> bool:
    """Kelime veya kelime grubunu başlık içinde sınırlarıyla arar."""
    return f" {keyword} " in f" {title} "


def story_priority(story: dict[str, Any]) -> int:
    """AI haberlerine teknoloji haberlerinden daha yüksek puan verir."""
    title = _normalize(story.get("title", ""))
    ai_score = sum(100 for keyword in AI_KEYWORDS if _keyword_matches(title, keyword))
    technology_score = sum(10 for keyword in TECHNOLOGY_KEYWORDS if _keyword_matches(title, keyword))
    return ai_score + technology_score


def is_technology_story(story: dict[str, Any]) -> bool:
    return story_priority(story) > 0


def filter_technology_stories(stories: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    """Başlığa göre AI öncelikli teknoloji hikâyelerini seçer."""
    matching = [
        (index, story)
        for index, story in enumerate(stories)
        if is_technology_story(story)
    ]
    matching.sort(key=lambda item: (-story_priority(item[1]), item[0]))
    return [story for _, story in matching[:limit]]
