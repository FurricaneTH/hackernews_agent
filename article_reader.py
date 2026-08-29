"""Basit ve güvenli makale metni çıkarıcı."""

from bs4 import BeautifulSoup
import requests


def read_article(url: str, max_chars: int = 50_000) -> str:
    """URL'deki HTML'den okunabilir metni çıkarır."""
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "hackernews-morning-agent/0.1"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "nav", "header", "footer", "form"]):
        element.decompose()

    container = soup.find("article") or soup.find("main") or soup.body or soup
    text = " ".join(container.get_text(" ", strip=True).split())

    if not text:
        raise ValueError("Sayfada okunabilir metin bulunamadı.")

    return text[:max_chars]

