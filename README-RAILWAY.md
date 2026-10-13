# PXPanel — Railway Infrastructure (v13.4.0-railway)

بازنویسی زیرساخت مخصوص Railway (دامنه خام `*.up.railway.app`).

## فایل‌ها
- `Dockerfile` — ایمیج Python 3.12 + healthcheck
- `railway.toml` — build/deploy/healthcheck
- `start.sh` — uvicorn با proxy-headers و WS keepalive
- `main.py` / `relay_vless.py` / `xhttp_siz10.py` / `speed_limit.py`

## دیپلوی روی Railway
1. ریپو را بساز یا این پوشه را push کن
2. New Project → Deploy from GitHub
3. Volume بساز و به مسیر `/data` وصل کن (DATA_DIR)
4. در Networking دامنه عمومی Generate کن
5. متغیرها (اختیاری):
   - `ADMIN_PASSWORD`
   - `SECRET_KEY`
   - `DATA_DIR=/data` (اگر volume جدا داری)

## نکات مهم edge
- یک replica کافی است (وضعیت WS در حافظه است)
- Serverless/sleep را خاموش نگه دار
- اگر پینگ از ایران نمی‌آید، مشکل از edge/اپراتور است نه فقط کد؛ منطقه سرویس را عوض کن یا دامنه را Remove و دوباره Add کن

## لوکال
```bash
bash start.sh
# یا
python main.py
```
