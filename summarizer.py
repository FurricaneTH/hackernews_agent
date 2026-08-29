"""OpenAI API ile Türkçe haber özeti üretir."""

import os

from openai import OpenAI


PROMPT = """Aşağıdaki Hacker News makalesini Türkçe ve detaylı biçimde özetle.

Şu başlıkları kullan:
1. Kısa özet
2. Temel fikir
3. Önemli ayrıntılar
4. Neden önemli?
5. Hacker News okuyucusu için değerlendirme

Yalnızca verilen metne dayan. Metinde bulunmayan bilgileri uydurma.
Teknik terimleri gerektiğinde kısa ve anlaşılır şekilde açıkla.

MAKALE METNİ:
"""


def summarize_article(article_text: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
        input=PROMPT + article_text,
        max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "2500")),
    )
    return response.output_text.strip()
