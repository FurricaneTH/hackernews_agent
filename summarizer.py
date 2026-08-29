"""OpenAI API ile kompakt Türkçe haber özeti üretir."""

import os

from openai import OpenAI


PROMPT = """Aşağıdaki Hacker News makalesini Türkçe, kompakt ama anlamlı biçimde özetle.

Şu başlıkları kullan:
1. Özet: 3-4 cümle
2. Önemli noktalar: En fazla 4 madde
3. Neden önemli?: 2-3 cümle
4. Terimler: Yalnızca gerekiyorsa en fazla 3 kısa açıklama

Yalnızca verilen metne dayan. Metinde bulunmayan bilgileri uydurma.
Gereksiz giriş, tekrar ve uzun arka plan anlatımı ekleme.

MAKALE METNİ:
"""


def summarize_article(article_text: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
        input=PROMPT + article_text,
        max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "1200")),
    )
    return response.output_text.strip()
