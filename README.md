<div align="center">

# 🚀 PXPanel

### دروازه مدرن تونل‌زنی · مدیریت کانفیگ · ربات تلگرام

**VLESS · XHTTP · Hysteria2 · TUIC · WireGuard · VMess · Trojan**

[![Version](https://img.shields.io/badge/version-13.4.0--railway-blue?style=for-the-badge)](https://github.com/pixonsybertik/pxpanel)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app/)
[![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)](#)

```text
Gateway · Subscription · Admin · Telegram Bot · Live Stats
```

[ویژگی‌ها](#-ویژگی‌ها) · [نصب سریع](#-نصب-سریع-روی-railway) · [پروتکل‌ها](#-پروتکل‌ها) · [ربات](#-ربات-تلگرام) · [متغیرها](#️-متغیرهای-محیطی)

<br/>

📡 **پشتیبانی:** [@Pixonal](https://t.me/Pixonal) &nbsp;|&nbsp;
📢 **کانال:** [logic_sec](https://t.me/logic_sec) &nbsp;|&nbsp;
▶ **یوتیوب:** [LogicSec](https://www.youtube.com/@LogicSec_YT)

</div>

---

## ✨ ویژگی‌ها

<table>
<tr>
<td width="50%" valign="top">

### 🔌 پروتکل و ترابرد
- **VLESS** WebSocket
- **XHTTP** (packet-up / stream-up / stream-one)

### 🎛️ پنل مدیریت
- داشبورد زنده (اتصال · ترافیک · آپتایم)
- ساخت دستی و خودکار
- **ویرایش تک‌کانفیگ** (دکمه مداد)
- گروه‌بندی · ساب · QR
- تم روشن / تیره · فارسی / English

</td>
<td width="50%" valign="top">

### 👥 سیستم ادمین
- اکانت ادمین جدا با سهمیه حجم
- انقضای زمانی حساب
- دسترسی سطح‌بندی‌شده به بخش‌ها
- ایزوله: ادمین فقط کانفیگ‌های خودش را می‌بیند
- مالک به همه کانفیگ‌ها دسترسی دارد

### 🤖 ربات تلگرام
- داشبورد و آمار
- **پینگ سرور** (تأخیر واقعی)
- ساخت سریع و ساخت دستی
- لیست · روشن/خاموش · حذف
- لینک VLESS و ساب

</td>
</tr>
</table>

### کنترل ترافیک
| مورد | توضیح |
|:-----|:------|
| حجم | KB / MB / GB · مقدار `0` = نامحدود |
| انقضا | بر حسب روز |
| سرعت | محدودیت پهنای باند (Mbps) |
| ساب | لینک اشتراک استاندارد + هدر `subscription-userinfo` |

---

## 🛠 نصب سریع روی Railway

### ۱) فورک و دیپلوی

```text
①  Fork این ریپازیتوری
②  Railway → New Project → Deploy from GitHub
③  ریپوی فورک‌شده را انتخاب کنید
```

### ۲) Volume دائمی

در سرویس Railway یک **Volume** بسازید و به مسیر زیر وصل کنید:

```bash
/data
```

بدون Volume، با هر ری‌استارت اطلاعات کانفیگ‌ها پاک می‌شود.

### ۳) دامنه عمومی

```text
Settings → Networking → Generate Domain
```

دامنه شبیه `xxx.up.railway.app` ساخته می‌شود و متغیر `RAILWAY_PUBLIC_DOMAIN` خودکار ست می‌شود.

### ۴) ورود به پنل

| مسیر | آدرس |
|:-----|:-----|
| داشبورد | `https://YOUR-DOMAIN/dashboard` |
| ورود | `https://YOUR-DOMAIN/login` |
| سلامت سرویس | `https://YOUR-DOMAIN/health` |

> رمز پیش‌فرض از متغیر `ADMIN_PASSWORD` خوانده می‌شود (در صورت عدم تنظیم، مقدار پیش‌فرض پنل اعمال می‌شود).

---

## 📁 ساختار پروژه

```text
pxpanel/
├── main.py              # هسته FastAPI · UI · API · ساب
├── relay_vless.py       # رله VLESS WebSocket
├── xhttp_siz10.py       # هندلر XHTTP
├── speed_limit.py       # محدودیت سرعت
├── telegram_bot.py      # ربات تلگرام (PX Bot)
├── start.sh             # استارت بهینه Railway
├── Dockerfile           # ایمیج دیپلوی
├── railway.toml         # تنظیم build / healthcheck
└── requirements.txt
```

### استارت مخصوص Railway

`start.sh` با این تنظیمات اجرا می‌شود:

- `0.0.0.0:$PORT`
- `proxy-headers` و trust به لبه Railway
- WebSocket ping / keep-alive
- یک worker (وضعیت اتصال در حافظه)

---

## 🔐 پروتکل‌ها

| پروتکل | نوع | پیشنهاد |
|:-------|:----|:--------|
| `vless-ws` | VLESS + WebSocket + TLS | ⭐ پیش‌فرض |
| `xhttp-packet-up` | XHTTP | موبایل / ناپایدار |
| `xhttp-stream-up` | XHTTP | پایدار |
| `xhttp-stream-one` | XHTTP | ساده |
| `vmess-ws` | VMess WS | سازگاری قدیمی |
| `trojan-ws` | Trojan WS | — |
| `hysteria2` / `tuic` | UDP-based | نیاز به کلاینت به‌روز |

**تنظیمات پیشنهادی لینک روی Railway**

```text
security  = tls
type      = ws
port      = 443
alpn      = http/1.1
fp        = chrome
sni/host  = دامنه عمومی Railway شما
```

---

## 🤖 ربات تلگرام

1. از [@BotFather](https://t.me/BotFather) ربات بسازید و **Token** را کپی کنید  
2. آیدی عددی خود را از [@userinfobot](https://t.me/userinfobot) بگیرید  
3. در پنل: **ربات تلگرام** → Token و Admin ID → ذخیره و فعال‌سازی  

| دکمه | کار |
|:-----|:----|
| 📊 داشبورد | آمار زنده |
| 📡 پینگ سرور | تأخیر تا `/health` |
| 🟢 لیست | مشاهده و مدیریت کانفیگ‌ها |
| ⚡ ساخت سریع | یک‌کلیکی |
| 🛠 ساخت دستی | نام · پروتکل · حجم · انقضا |

---

## 👤 ادمین‌ها

```text
مالک (Owner)
  └── همه کانفیگ‌ها · همه بخش‌ها · ساخت ادمین

ادمین (Sub-admin)
  ├── فقط کانفیگ‌های با owner_id خودش
  ├── سقف حجم (سهمیه)
  ├── انقضای حساب
  └── دسترسی انتخابی: داشبورد / کانفیگ / ساخت / آمار / ...
```

در لیست کانفیگ‌ها، ادمین کانفیگ‌های مالک را **نمی‌بیند**.

---

## ⚙️ متغیرهای محیطی

| متغیر | توضیح | پیش‌فرض |
|:------|:------|:--------|
| `PORT` | پورت گوش‌دادن (Railway خودکار) | `8000` |
| `ADMIN_PASSWORD` | رمز ورود مالک | — |
| `SECRET_KEY` | کلید سشن (در صورت خالی، خودکار) | — |
| `DATA_DIR` | مسیر ذخیره | `/data` |
| `RAILWAY_PUBLIC_DOMAIN` | دامنه عمومی | توسط Railway |
| `TELEGRAM_BOT_TOKEN` | توکن ربات (اختیاری) | — |
| `TELEGRAM_ADMIN_IDS` | آیدی عددی ادمین‌ها | — |

---

## 🖥 اجرای لوکال

```bash
# کلون
git clone https://github.com/pixonsybertik/pxpanel.git
cd pxpanel

# وابستگی
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# اجرا
bash start.sh
# یا
python main.py
```

پنل روی `http://127.0.0.1:8000` در دسترس است.

---

## 📡 سابسکریپشن

```text
تک‌کانفیگ     https://DOMAIN/sub/{uuid}
همه           https://DOMAIN/sub-all
اطلاعات       https://DOMAIN/info/{uuid}
```

هدرهای استاندارد (`subscription-userinfo`) برای نمایش حجم و انقضا در کلاینت‌هایی مثل v2rayNG · Streisand · Hiddify پشتیبانی می‌شود.

---

## ⚠️ نکات مهم

> **کلاینت را به‌روز نگه دارید.**  
> برای XHTTP، Hysteria2 و TUIC آخرین نسخه نرم‌افزار اتصال لازم است.

> **Volume را فراموش نکنید.**  
> بدون Volume دائمی، با ری‌استارت Railway داده‌ها از بین می‌رود.

> **دامنه خام Railway**  
> روی برخی اپراتورهای موبایل ایران، WebSocket روی `*.up.railway.app` ممکن است ناپایدار باشد. در این حالت منطقه سرویس را عوض کنید یا از دامنه اختصاصی استفاده کنید.

> **یک Replica**  
> به‌خاطر ذخیره اتصال در حافظه، یک instance کافی و توصیه‌شده است.

---

## 🗺️ نقشه راه

- [x] هسته VLESS / XHTTP روی Railway  
- [x] داشبورد و تم تیره  
- [x] ربات تلگرام با پینگ و ساخت دستی  
- [x] ادمین ایزوله + سهمیه حجم  
- [x] ویرایش تک‌کانفیگ از جدول  
- [ ] اعلان تلگرام هنگام اتمام حجم  
- [ ] API عمومی محدود برای فروشنده‌ها  

---

## 📄 مجوز و مسئولیت

این پروژه برای **یادگیری و استفاده شخصی** ارائه شده است.  
رعایت قوانین کشور محل استفاده بر عهده کاربر است.

---

<div align="center">

**PXPanel** · ساخته‌شده با FastAPI · بهینه برای Railway

اگر مفید بود ⭐ بدهید

<br/>

[![Telegram](https://img.shields.io/badge/Telegram-@Pixonal-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/Pixonal)
[![Channel](https://img.shields.io/badge/Channel-logic__sec-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/logic_sec)

</div>
