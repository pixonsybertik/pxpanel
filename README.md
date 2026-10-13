<p align="center">
  <img src="https://img.shields.io/badge/PXPANEL-v13.4.0--railway-0ea5e9?style=for-the-badge&labelColor=0f172a" alt="PXPanel"/>
</p>

<h1 align="center">PXPanel</h1>

<p align="center">
  <b>دروازه سریع · امن · مدرن برای تونل‌زنی نسل جدید</b><br/>
  <sub>VLESS · XHTTP · Hysteria2 · TUIC · WireGuard · Dashboard · Telegram Bot</sub>
</p>

<p align="center">
  <a href="#-ویژگی‌های-اصلی"><img src="https://img.shields.io/badge/Features-Complete-22c55e?style=flat-square" alt="features"/></a>
  <a href="#-دیپلوی-یک‌کلیکی-روی-railway"><img src="https://img.shields.io/badge/Railway-Ready-0B0D0E?style=flat-square&logo=railway&logoColor=white" alt="railway"/></a>
  <a href="#-ربات-تلگرام-px-bot"><img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white" alt="bot"/></a>
  <a href="#-پروتکل‌ها"><img src="https://img.shields.io/badge/Protocols-12+-8b5cf6?style=flat-square" alt="protocols"/></a>
  <a href="#-امنیت--ایزوله‌سازی"><img src="https://img.shields.io/badge/Admin-Isolated-f59e0b?style=flat-square" alt="admin"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="python"/>
  <img src="https://img.shields.io/badge/FastAPI-Async-009688?style=flat-square&logo=fastapi&logoColor=white" alt="fastapi"/>
  <img src="https://img.shields.io/badge/Uvicorn-ASGI-499848?style=flat-square" alt="uvicorn"/>
  <img src="https://img.shields.io/badge/UI-Dark%20%2F%20Light-64748b?style=flat-square" alt="ui"/>
  <img src="https://img.shields.io/badge/i18n-FA%20%7C%20EN-e11d48?style=flat-square" alt="i18n"/>
</p>

---

```text
┌─────────────────────────────────────────────────────────────┐
│  PXPanel  ·  Gateway  ·  Subscription  ·  Live Ops         │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │
│  │ Dashboard│   │  Configs │   │  Admins  │   │  TG Bot │ │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬────┘ │
│       │              │              │              │       │
│       └──────────────┴──────┬───────┴──────────────┘       │
│                             ▼                               │
│              VLESS / XHTTP / Hysteria2 / TUIC               │
│                     Railway Edge · TLS 443                  │
└─────────────────────────────────────────────────────────────┘
```

<p align="center">
  <a href="https://t.me/Pixonal"><strong>پشتیبانی</strong></a> ·
  <a href="https://t.me/logic_sec"><strong>کانال</strong></a> ·
  <a href="https://www.youtube.com/@LogicSec_YT"><strong>یوتیوب</strong></a>
</p>

---

## 🎯 این پنل چیست؟

**PXPanel** یک پنل مدیریت کامل برای ساخت، توزیع و کنترل کانفیگ‌های پروکسی است؛ مخصوص دیپلوی روی **Railway** طراحی شده و شامل:

| لایه | قابلیت |
|:-----|:-------|
| **Gateway** | رله VLESS WebSocket و موتور XHTTP |
| **Control Plane** | داشبورد، آمار زنده، لاگ، گروه‌بندی |
| **Subscription** | لینک ساب استاندارد + هدر حجم/انقضا |
| **Multi-Admin** | ادمین ایزوله با سهمیه حجم و دسترسی سطح‌بندی |
| **Telegram Ops** | ربات اختصاصی برای ساخت، پینگ و مدیریت |

> مناسب برای مدیریت شخصی، تیم کوچک و فروشنده‌هایی که به **ایزوله‌سازی ادمین** و **سهمیه ترافیک** نیاز دارند.

---

## ✨ ویژگی‌های اصلی

<details open>
<summary><b>🔌 پروتکل و شبکه</b></summary>
<br/>

- **VLESS + WebSocket + TLS** (پیشنهادی روی Railway)
- **XHTTP** در سه حالت: `packet-up` · `stream-up` · `stream-one`
- Hysteria2 · TUIC · WireGuard
- VMess WS · Trojan WS · Shadowsocks
- SOCKS5 و HTTP Proxy داخلی
- Fingerprint (uTLS) · ALPN قابل تنظیم · پورت سفارشی

</details>

<details open>
<summary><b>🎛️ پنل وب</b></summary>
<br/>

- داشبورد زنده: اتصالات · ترافیک · تعداد کانفیگ · آپتایم
- ساخت **دستی** و **خودکار (پیشنهادی)**
- **ویرایش تک‌کانفیگ** با دکمه مداد روی هر ردیف
- مدیریت گروهی، جستجو، انتقال دسته‌ای
- صفحات ساب حرفه‌ای + QR
- تم تیره / روشن · رابط فارسی و English

</details>

<details open>
<summary><b>👥 ادمین و امنیت</b></summary>
<br/>

- اکانت ادمین جدا با نام کاربری / رمز / برچسب
- **سهمیه حجم** و **انقضای زمانی** برای هر ادمین
- دسترسی بخش‌به‌بخش: داشبورد، کانفیگ، ساخت، آمار، لاگ، ربات، اخبار، ادمین‌ها
- ادمین **فقط کانفیگ‌های خودش** را می‌بیند؛ به کانفیگ‌های مالک دسترسی ندارد
- قفل ورود پس از تلاش ناموفق · بک‌آپ / بازیابی

</details>

<details open>
<summary><b>🤖 ربات تلگرام (PX Bot)</b></summary>
<br/>

| قابلیت | توضیح |
|:-------|:------|
| داشبورد | آمار لحظه‌ای پنل |
| پینگ سرور | اندازه‌گیری تأخیر واقعی تا `/health` |
| ساخت سریع | یک‌کلیک |
| ساخت دستی | ویزارد: نام → پروتکل → حجم → انقضا |
| مدیریت | لیست · لینک · ساب · روشن/خاموش · حذف |
| استقرار | Webhook یا Polling روی Railway |

</details>

---

## 🚀 دیپلوی یک‌کلیکی روی Railway

### پیش‌نیاز
- حساب [Railway](https://railway.app)
- اکانت GitHub

### مراحل

```bash
# 1) فورک ریپازیتوری
# 2) Railway → New Project → Deploy from GitHub repo
# 3) Volume بسازید و Mount Path را بگذارید روی:
/data

# 4) دامنه عمومی
Settings → Networking → Generate Domain
```

### بعد از دیپلوی

| مسیر | کاربرد |
|:-----|:-------|
| `/login` | ورود به پنل |
| `/dashboard` | داشبورد مدیریت |
| `/health` | بررسی سلامت سرویس |
| `/sub/{uuid}` | لینک ساب تک‌کانفیگ |

```bash
https://YOUR-APP.up.railway.app/dashboard
```

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production_Ready-22c55e?style=for-the-badge&labelColor=052e16" alt="ready"/>
</p>

---

## 🏗 معماری

```text
                    ┌──────────────────────┐
   Client Apps      │   Railway Edge TLS   │
  (v2rayNG, ...) ──►│   *.up.railway.app   │
                    └──────────┬───────────┘
                               │ HTTPS / WSS
                    ┌──────────▼───────────┐
                    │     PXPanel Core     │
                    │  FastAPI + Uvicorn   │
                    │  · Dashboard / API   │
                    │  · Subscription      │
                    │  · Admin Sessions    │
                    └───┬─────────────┬────┘
                        │             │
              ┌─────────▼──┐    ┌─────▼────────┐
              │ relay_vless│    │  xhttp_siz10 │
              │  /ws/{id}  │    │ /xhttp-siz10 │
              └─────────┬──┘    └─────┬────────┘
                        │             │
                        └──────┬──────┘
                               ▼
                        Destination TCP
```

| فایل | نقش |
|:-----|:----|
| `main.py` | هسته API · UI · سشن · ساب · ادمین |
| `relay_vless.py` | رله VLESS روی WebSocket |
| `xhttp_siz10.py` | موتور XHTTP |
| `speed_limit.py` | محدودیت پهنای باند |
| `telegram_bot.py` | ربات عملیاتی |
| `start.sh` | استارت بهینه edge Railway |
| `Dockerfile` / `railway.toml` | بیلد و healthcheck |

---

## 📡 پروتکل‌ها

| شناسه | نام نمایشی | وضعیت |
|:------|:-----------|:------|
| `vless-ws` | VLESS WebSocket | ⭐ پیشنهادی |
| `xhttp-packet-up` | XHTTP Packet Up | پایدار روی موبایل |
| `xhttp-stream-up` | XHTTP Stream Up | استریم پیوسته |
| `xhttp-stream-one` | XHTTP Stream One | ساده |
| `vmess-ws` | VMess WebSocket | سازگاری |
| `trojan-ws` | Trojan WebSocket | — |
| `shadowsocks` | Shadowsocks | — |
| `hysteria2` | Hysteria2 | کلاینت جدید |
| `tuic` | TUIC | کلاینت جدید |
| `wireguard` | WireGuard | — |

### پروفایل پیشنهادی لینک (Railway)

```text
protocol   = vless-ws
port       = 443
security   = tls
network    = ws
alpn       = http/1.1
fingerprint= chrome
host / sni = YOUR-APP.up.railway.app
path       = /ws/{uuid}
```

---

## 👤 مدل دسترسی

```text
OWNER
 ├─ تمام کانفیگ‌ها
 ├─ ساخت / ویرایش / حذف همه
 ├─ مدیریت ادمین‌ها و سهمیه
 └─ تنظیمات سیستم و ربات

ADMIN (ایزوله)
 ├─ فقط کانفیگ‌هایی با owner_id = خودش
 ├─ سقف حجم (quota) و تاریخ انقضا
 ├─ دسترسی بخش‌های انتخاب‌شده
 └─ بدون دید به کانفیگ‌های مالک
```

در جدول کانفیگ‌ها، هر ردیف دکمه **ویرایش (مداد)** دارد تا همان یک کانفیگ را سریع تغییر دهید.

---

## ⚙️ متغیرهای محیطی

| متغیر | الزامی | توضیح |
|:------|:------:|:------|
| `PORT` | خودکار | پورت سرویس Railway |
| `ADMIN_PASSWORD` | توصیه‌شده | رمز ورود مالک |
| `SECRET_KEY` | اختیاری | کلید امضای سشن (در صورت خالی خودکار) |
| `DATA_DIR` | توصیه‌شده | مسیر Volume — معمولاً `/data` |
| `RAILWAY_PUBLIC_DOMAIN` | خودکار | دامنه عمومی سرویس |
| `TELEGRAM_BOT_TOKEN` | اختیاری | توکن ربات |
| `TELEGRAM_ADMIN_IDS` | اختیاری | آیدی عددی ادمین(ها) |

---

## 🖥 اجرای محلی

```bash
git clone https://github.com/pixonsybertik/pxpanel.git
cd pxpanel

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

bash start.sh
# یا: python main.py
```

سرویس روی آدرس زیر بالا می‌آید:

```text
http://127.0.0.1:8000
```

---

## 📦 سابسکریپشن

| نوع | مسیر |
|:----|:-----|
| تک‌کانفیگ | `/sub/{uuid}` |
| همه | `/sub-all` |
| صفحه اطلاعات | `/info/{uuid}` |

هدرهای استاندارد کلاینت پشتیبانی می‌شوند:

```http
subscription-userinfo: upload=0; download=...; total=...; expire=...
profile-title: ...
profile-update-interval: 12
```

سازگار با **v2rayNG · Streisand · Hiddify · NekoBox · MahsaNG** و مشابه.

---

## ✅ چک‌لیست بعد از دیپلوی

- [ ] Volume روی `/data` وصل است
- [ ] دامنه عمومی Generate شده
- [ ] `/health` پاسخ `ok` می‌دهد
- [ ] ورود به `/login` موفق است
- [ ] یک کانفیگ تست ساخته و در کلاینت Import شده
- [ ] (اختیاری) ربات با Token و Admin ID فعال شده

---

## ⚠️ نکات عملیاتی

> **Volume اجباری است.** بدون آن، با هر ری‌استارت وضعیت پنل از بین می‌رود.

> **یک Replica.** وضعیت اتصالات در حافظه است؛ برای این معماری یک instance کافی است.

> **کلاینت به‌روز.** برای XHTTP / Hysteria2 / TUIC حتماً آخرین نسخه اپ را استفاده کنید.

> **پایداری روی موبایل ایران.** دامنه خام `*.up.railway.app` گاهی روی بعضی اپراتورها برای WebSocket ناپایدار است. در این حالت منطقه سرویس را عوض کنید یا دامنه اختصاصی بگذارید.

---

## 🗺️ نقشه راه

| وضعیت | مورد |
|:-----:|:-----|
| ✅ | هسته VLESS / XHTTP روی Railway |
| ✅ | داشبورد · تم · i18n |
| ✅ | ربات با پینگ و ساخت دستی |
| ✅ | ادمین ایزوله + سهمیه |
| ✅ | ویرایش تک‌کانفیگ از UI |
| 🔜 | اعلان اتمام حجم در تلگرام |
| 🔜 | API محدود برای فروشنده |
| 🔜 | گزارش مصرف روزانه |

---

## 📄 مسئولیت استفاده

این پروژه برای **آموزش و استفاده شخصی** منتشر شده است.  
رعایت قوانین محل استفاده بر عهده کاربر نهایی است. توسعه‌دهنده مسئول سوءاستفاده نیست.

---

<p align="center">
  <b>PXPanel</b><br/>
  <sub>FastAPI · Railway · Production-minded</sub>
</p>

<p align="center">
  <a href="https://t.me/Pixonal"><img src="https://img.shields.io/badge/Support-%40Pixonal-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="support"/></a>
  <a href="https://t.me/logic_sec"><img src="https://img.shields.io/badge/Channel-logic__sec-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="channel"/></a>
</p>

<p align="center">
  اگر پروژه برایتان مفید بود، به ریپازیتوری <b>⭐ Star</b> بدهید.
</p>
