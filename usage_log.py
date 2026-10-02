"""OpenAI çağrılarının token kullanımını ve tahmini ücretini kaydeder."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_LOG_NAME = "usage_log.jsonl"


def log_path() -> Path:
    """Kullanım kaydının tutulduğu JSONL dosyasının yolunu döndürür."""
    configured = os.getenv("USAGE_LOG_PATH")
    if configured:
        return Path(configured).expanduser()
    return Path(__file__).with_name(DEFAULT_LOG_NAME)


def _price_per_million(variable: str) -> float | None:
    raw = os.getenv(variable)
    if raw is None or not raw.strip():
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _field(usage: Any, *names: str) -> int:
    """Responses API usage nesnesinden ya da sözlüğünden token sayısını okur."""
    for name in names:
        value = usage.get(name) if isinstance(usage, dict) else getattr(usage, name, None)
        if isinstance(value, (int, float)):
            return int(value)
    return 0


def estimate_cost(input_tokens: int, output_tokens: int) -> float | None:
    """Fiyatlar yapılandırılmışsa çağrının tahmini USD maliyetini hesaplar."""
    input_price = _price_per_million("OPENAI_INPUT_PRICE_PER_1M")
    output_price = _price_per_million("OPENAI_OUTPUT_PRICE_PER_1M")
    if input_price is None and output_price is None:
        return None
    cost = input_tokens / 1_000_000 * (input_price or 0.0)
    cost += output_tokens / 1_000_000 * (output_price or 0.0)
    return round(cost, 6)


def record_usage(model: str, usage: Any, label: str = "") -> dict[str, Any]:
    """Bir API çağrısının kullanımını JSONL dosyasına ekler ve kaydı döndürür."""
    input_tokens = _field(usage, "input_tokens", "prompt_tokens")
    output_tokens = _field(usage, "output_tokens", "completion_tokens")
    total_tokens = _field(usage, "total_tokens") or input_tokens + output_tokens

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": model,
        "label": label,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": estimate_cost(input_tokens, output_tokens),
    }

    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def read_recent(limit: int = 10) -> list[dict[str, Any]]:
    """En son kaydedilen çağrıları yeniden eskiye doğru sıralı döndürür."""
    path = log_path()
    if not path.exists():
        return []

    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    records.reverse()
    return records[:limit] if limit > 0 else records


def _format_cost(cost: float | None) -> str:
    return f"${cost:.6f}" if isinstance(cost, (int, float)) else "fiyat yok"


def format_records(records: list[dict[str, Any]]) -> str:
    """Kullanım kayıtlarını terminalde okunabilir bir tabloya çevirir."""
    if not records:
        return (
            "Henüz API kullanım kaydı yok.\n"
            f"Kayıt dosyası: {log_path()}"
        )

    lines = [
        f"{'TARİH (UTC)':<25} {'MODEL':<16} {'GİRDİ':>8} {'ÇIKTI':>8} {'TOPLAM':>8}  {'MALİYET':<12} ETİKET",
        "-" * 100,
    ]
    for record in records:
        lines.append(
            f"{record.get('timestamp', '-'):<25} "
            f"{str(record.get('model', '-'))[:16]:<16} "
            f"{record.get('input_tokens', 0):>8} "
            f"{record.get('output_tokens', 0):>8} "
            f"{record.get('total_tokens', 0):>8}  "
            f"{_format_cost(record.get('estimated_cost_usd')):<12} "
            f"{record.get('label', '')}"
        )

    lines.append("-" * 100)
    lines.append(summarize_records(records))
    if any(record.get("estimated_cost_usd") is None for record in records):
        lines.append(
            "Not: Maliyet için .env dosyasına OPENAI_INPUT_PRICE_PER_1M ve "
            "OPENAI_OUTPUT_PRICE_PER_1M değerlerini yaz."
        )
    lines.append(f"Kayıt dosyası: {log_path()}")
    return "\n".join(lines)


def summarize_records(records: list[dict[str, Any]]) -> str:
    """Verilen kayıtların token ve maliyet toplamını tek satırda özetler."""
    total_tokens = sum(int(record.get("total_tokens", 0) or 0) for record in records)
    costs = [
        record.get("estimated_cost_usd")
        for record in records
        if isinstance(record.get("estimated_cost_usd"), (int, float))
    ]
    cost_text = f"${sum(costs):.6f}" if costs else "fiyat yapılandırılmadı"
    return f"{len(records)} çağrı | {total_tokens} token | tahmini maliyet: {cost_text}"
