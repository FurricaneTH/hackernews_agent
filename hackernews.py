"""Hacker News resmi Firebase API istemcisi."""

from typing import Any

import requests


BASE_URL = "https://hacker-news.firebaseio.com/v0"


def _get_json(path: str) -> Any:
    response = requests.get(f"{BASE_URL}/{path}.json", timeout=20)
    response.raise_for_status()
    return response.json()


def get_top_stories(count: int = 3) -> list[dict[str, Any]]:
    """Güncel top stories listesinden ilk count adet hikâyeyi getirir."""
    story_ids = _get_json("topstories")
    stories: list[dict[str, Any]] = []

    for story_id in story_ids[:count]:
        story = _get_json(f"item/{story_id}")
        if story and story.get("type") == "story" and not story.get("dead"):
            stories.append(story)

    return stories

