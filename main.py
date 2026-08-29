"""Hacker News sabah bülteninin ana akışı."""

import argparse
import html
import os
from pathlib import Path

from hackernews import get_top_stories


def build_email(stories: list[dict], summaries: list[str]) -> str:
    sections = []
    for index, (story, summary) in enumerate(zip(stories, summaries), start=1):
        title = html.escape(story.get("title", "Başlıksız haber"))
        url = html.escape(story.get("url", ""), quote=True)
        sections.append(
            f"<h2>{index}. {title}</h2>"
            f"<p><a href=\"{url}\">Makaleyi aç</a></p>"
            f"<div>{html.escape(summary).replace(chr(10), '<br>')}</div>"
        )
    return "<html><body><h1>Hacker News Sabah Bülteni</h1>" + "".join(sections) + "</body></html>"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="E-posta göndermeden haberleri göster")
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).with_name(".env"))
    except ModuleNotFoundError:
        pass
    story_count = int(os.getenv("STORY_COUNT", "3"))
    stories = get_top_stories(count=story_count)

    if not stories:
        print("Haber bulunamadı.")
        return

    if args.preview:
        for index, story in enumerate(stories, start=1):
            print(f"{index}. {story.get('title', 'Başlıksız haber')}")
            print(f"   URL: {story.get('url', 'Hacker News bağlantısı yok')}")
        return

    from article_reader import read_article
    from summarizer import summarize_article
    from email_sender import send_email

    summaries = []
    for index, story in enumerate(stories, start=1):
        url = story.get("url")
        if not url:
            summaries.append("Bu hikâyenin harici bir makale bağlantısı yok.")
            continue
        try:
            article_text = read_article(url)
            summaries.append(summarize_article(article_text))
            print(f"{index}. haber özetlendi.")
        except Exception as exc:
            summaries.append(f"Makale okunamadı veya özetlenemedi: {exc}")
            print(f"{index}. haber için hata: {exc}")

    if not args.preview:
        send_email("Hacker News Sabah Bülteni", build_email(stories, summaries))
        print("Bülten e-posta olarak gönderildi.")


if __name__ == "__main__":
    main()
