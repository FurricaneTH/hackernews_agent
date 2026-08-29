# Hacker News Morning Agent

Hacker News'in güncel üst sıralarındaki haberleri alıp Türkçe detaylı özetleyen kişisel ajan.

## Aşamalar

1. Hacker News API'den ilk haberleri alma (tamamlandı)
2. Haber makalelerinin metnini çıkarma (tamamlandı)
3. OpenAI API ile Türkçe özetleme (Luna modeli; kredi bekliyor)
4. E-posta gönderme (SMTP ayarları bekliyor)
5. Her gün 09:00 zamanlama (daha sonra)

## İlk çalıştırma

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

API ve e-posta ayarlarını `.env.example` dosyasını `.env` olarak kopyalayıp dolduracağız.

Sadece Hacker News bağlantısını test etmek için:

```bash
python main.py --preview
```
