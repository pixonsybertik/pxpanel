# telegram_bot.py — PX Bot (professional)
# قابلیت‌ها: داشبورد، لیست، ساخت سریع/دستی، پینگ دامنه، ساب، حذف، فعال/غیرفعال

from __future__ import annotations

import asyncio
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import httpx

from main import (
    LINKS,
    LINKS_LOCK,
    make_link,
    remove_link,
    set_link_active,
    vless_link_for_link,
    get_host,
    fmt_bytes,
    is_link_allowed,
    is_link_expired,
    logger,
    PROTOCOLS,
    DEFAULT_PROTOCOL,
    FINGERPRINTS,
    DEFAULT_FINGERPRINT,
    DEFAULT_ALPN_BY_PROTOCOL,
    DEFAULT_PORT,
    parse_size_to_bytes,
    stats,
    connections,
    activity_logs,
    CONFIG,
    DATA_DIR,
    unique_ips_for_uuid,
)

BOT_NAME = "پی ایکس بات"
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
_admin_ids_raw = os.environ.get("TELEGRAM_ADMIN_IDS", "").strip()
ADMIN_IDS = {
    int(x)
    for x in _admin_ids_raw.replace(" ", "").split(",")
    if x.isdigit()
} if _admin_ids_raw else set()
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

PAGE_SIZE = 6
_client: httpx.AsyncClient | None = None
_poll_task: asyncio.Task | None = None
_running = False
_pending: dict = {}  # chat_id -> wizard state

PROTOCOL_LABELS = {
    "vless-ws": "🟢 VLESS · WebSocket",
    "xhttp-packet-up": "⚡ XHTTP packet-up",
    "xhttp-stream-up": "⚡ XHTTP stream-up",
    "xhttp-stream-one": "⚡ XHTTP stream-one",
    "vmess-ws": "🔵 VMess · WS",
    "trojan-ws": "🟠 Trojan · WS",
    "shadowsocks": "🟣 Shadowsocks",
    "hysteria2": "🚀 Hysteria2",
    "tuic": "💎 TUIC",
}


def _is_admin(chat_id: int) -> bool:
    return (not ADMIN_IDS) or (chat_id in ADMIN_IDS)


async def _client_get() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=30.0)
    return _client


async def _call(method: str, **params):
    if not API_BASE:
        return None
    c = await _client_get()
    r = await c.post(f"{API_BASE}/{method}", json=params)
    try:
        return r.json()
    except Exception:
        return None


async def _send(chat_id: int, text: str, kb: dict | None = None, parse_mode: str = "HTML"):
    payload = {
        "chat_id": chat_id,
        "text": text[:4000],
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }
    if kb:
        payload["reply_markup"] = kb
    return await _call("sendMessage", **payload)


async def _edit(chat_id: int, message_id: int, text: str, kb: dict | None = None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text[:4000],
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if kb:
        payload["reply_markup"] = kb
    return await _call("editMessageText", **payload)


async def _answer_cb(cb_id: str, text: str = "", alert: bool = False):
    return await _call(
        "answerCallbackQuery",
        callback_query_id=cb_id,
        text=(text or "")[:200],
        show_alert=alert,
    )


def _kb(rows: list) -> dict:
    return {"inline_keyboard": rows}


def _main_menu() -> dict:
    return _kb([
        [{"text": "📊 داشبورد", "callback_data": "stats"},
         {"text": "📡 پینگ سرور", "callback_data": "ping"}],
        [{"text": "🟢 لیست کانفیگ‌ها", "callback_data": "list:0"},
         {"text": "🔌 اتصالات", "callback_data": "conns"}],
        [{"text": "⚡ ساخت سریع", "callback_data": "quick"},
         {"text": "🛠 ساخت دستی", "callback_data": "manual"}],
        [{"text": "📜 لاگ", "callback_data": "logs"},
         {"text": "🔄 منو", "callback_data": "menu"}],
    ])


def _host() -> str:
    return (
        os.environ.get("RAILWAY_PUBLIC_DOMAIN")
        or CONFIG.get("host")
        or "localhost"
    )


async def _ping_host() -> str:
    host = _host()
    url = f"https://{host}/health"
    t0 = time.perf_counter()
    try:
        c = await _client_get()
        r = await c.get(url, timeout=12.0)
        ms = int((time.perf_counter() - t0) * 1000)
        ok = r.status_code < 500
        body = ""
        try:
            body = r.json()
        except Exception:
            body = r.text[:80]
        status = "✅ آنلاین" if ok else "⚠️ خطا"
        return (
            f"📡 <b>پینگ سرور</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"دامنه: <code>{host}</code>\n"
            f"وضعیت: {status}\n"
            f"HTTP: <code>{r.status_code}</code>\n"
            f"تأخیر: <b>{ms} ms</b>\n"
            f"پاسخ: <code>{body}</code>\n"
            f"━━━━━━━━━━━━━━\n"
            f"⏱ {datetime.now().strftime('%H:%M:%S')}"
        )
    except Exception as e:
        ms = int((time.perf_counter() - t0) * 1000)
        return (
            f"📡 <b>پینگ سرور</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"دامنه: <code>{host}</code>\n"
            f"وضعیت: ❌ قطع\n"
            f"تأخیر تا خطا: <b>{ms} ms</b>\n"
            f"خطا: <code>{type(e).__name__}: {e}</code>"
        )


def _stats_text() -> str:
    host = _host()
    n_links = len(LINKS)
    n_on = sum(1 for L in LINKS.values() if is_link_allowed(L))
    n_conn = len(connections)
    traffic = int(stats.get("total_bytes") or 0)
    return (
        f"📊 <b>داشبورد {BOT_NAME}</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"🌐 دامنه: <code>{host}</code>\n"
        f"📦 کانفیگ‌ها: <b>{n_links}</b> (فعال: {n_on})\n"
        f"🔌 اتصال زنده: <b>{n_conn}</b>\n"
        f"📈 ترافیک کل: <b>{fmt_bytes(traffic)}</b>\n"
        f"━━━━━━━━━━━━━━"
    )


def _links_page(page: int):
    items = sorted(
        LINKS.items(),
        key=lambda kv: kv[1].get("created_at") or "",
        reverse=True,
    )
    total = len(items)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    slice_ = items[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]
    rows = []
    for uid, L in slice_:
        name = L.get("label") or uid[:8]
        on = is_link_allowed(L)
        dot = "🟢" if on else "🔴"
        rows.append([{"text": f"{dot} {name}", "callback_data": f"view:{uid}"}])
    nav = []
    if page > 0:
        nav.append({"text": "⬅️", "callback_data": f"list:{page-1}"})
    nav.append({"text": f"{page+1}/{pages}", "callback_data": "noop"})
    if page < pages - 1:
        nav.append({"text": "➡️", "callback_data": f"list:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "⚡ ساخت سریع", "callback_data": "quick"},
                 {"text": "🏠 منو", "callback_data": "menu"}])
    text = f"🟢 <b>لیست کانفیگ‌ها</b> · {total} مورد"
    return text, _kb(rows)


def _detail_kb(uid: str, active: bool) -> dict:
    return _kb([
        [{"text": "🔗 لینک VLESS", "callback_data": f"link:{uid}"},
         {"text": "📡 ساب", "callback_data": f"sub:{uid}"}],
        [{"text": "⏸ خاموش" if active else "▶️ روشن", "callback_data": f"tog:{uid}"},
         {"text": "🗑 حذف", "callback_data": f"del:{uid}"}],
        [{"text": "🔙 لیست", "callback_data": "list:0"},
         {"text": "🏠 منو", "callback_data": "menu"}],
    ])


async def _handle_start(chat_id: int):
    if not _is_admin(chat_id):
        await _send(chat_id, "⛔️ دسترسی ندارید.")
        return
    await _send(
        chat_id,
        f"سلام 👋\nبه <b>{BOT_NAME}</b> خوش آمدید.\nاز منوی زیر استفاده کنید.",
        _main_menu(),
    )


async def _handle_callback(cb: dict):
    chat_id = cb["message"]["chat"]["id"]
    mid = cb["message"]["message_id"]
    data = cb.get("data") or ""
    cid = cb["id"]

    if not _is_admin(chat_id):
        await _answer_cb(cid, "دسترسی ندارید", alert=True)
        return

    if data == "noop":
        await _answer_cb(cid)
        return

    if data in ("menu", "start"):
        await _answer_cb(cid)
        await _edit(chat_id, mid, f"<b>{BOT_NAME}</b>\nمنوی اصلی:", _main_menu())
        return

    if data == "stats":
        await _answer_cb(cid)
        await _edit(chat_id, mid, _stats_text(), _main_menu())
        return

    if data == "ping":
        await _answer_cb(cid, "در حال پینگ...")
        txt = await _ping_host()
        await _edit(chat_id, mid, txt, _kb([[{"text": "🔄 دوباره", "callback_data": "ping"},
                                            {"text": "🏠 منو", "callback_data": "menu"}]]))
        return

    if data.startswith("list:"):
        page = int(data.split(":")[1])
        await _answer_cb(cid)
        t, kb = _links_page(page)
        await _edit(chat_id, mid, t, kb)
        return

    if data == "conns":
        await _answer_cb(cid)
        lines = [f"🔌 <b>اتصالات زنده:</b> {len(connections)}"]
        for i, (cid_, c) in enumerate(list(connections.items())[:15]):
            lines.append(
                f"• <code>{str(c.get('uuid',''))[:8]}</code> · {c.get('ip','?')} · {c.get('transport','')}"
            )
        if not connections:
            lines.append("اتصالی نیست.")
        await _edit(chat_id, mid, "\n".join(lines), _main_menu())
        return

    if data == "logs":
        await _answer_cb(cid)
        logs = list(activity_logs)[-12:] if activity_logs else []
        if not logs:
            txt = "لاگی نیست."
        else:
            txt = "📜 <b>آخرین لاگ‌ها</b>\n" + "\n".join(
                f"• {x.get('msg') or x.get('message') or x}" for x in logs
            )
        await _edit(chat_id, mid, txt[:4000], _main_menu())
        return

    if data == "quick":
        await _answer_cb(cid, "در حال ساخت...")
        try:
            uid, link = await make_link(
                label=f"tg-{int(time.time())%100000}",
                limit_bytes=0,
                protocol=DEFAULT_PROTOCOL,
                fingerprint=DEFAULT_FINGERPRINT,
                alpn="http/1.1",
                port=443,
                owner_id=None,
            )
            host = _host()
            vless = vless_link_for_link(link, uid, host)
            sub = f"https://{host}/sub/{uid}"
            await _edit(
                chat_id,
                mid,
                f"✅ <b>کانفیگ ساخته شد</b>\n"
                f"نام: <code>{link.get('label')}</code>\n"
                f"پروتکل: {link.get('protocol')}\n\n"
                f"<code>{vless}</code>\n\n"
                f"📡 ساب:\n<code>{sub}</code>",
                _detail_kb(uid, True),
            )
        except Exception as e:
            await _edit(chat_id, mid, f"❌ خطا: {e}", _main_menu())
        return

    if data == "manual":
        await _answer_cb(cid)
        _pending[chat_id] = {"step": "label", "data": {}}
        await _edit(
            chat_id,
            mid,
            "🛠 <b>ساخت دستی</b>\n"
            "نام کانفیگ را بفرستید:\n"
            "<i>(یا /cancel برای انصراف)</i>",
            _kb([[{"text": "❌ انصراف", "callback_data": "menu"}]]),
        )
        return

    if data.startswith("view:"):
        uid = data.split(":", 1)[1]
        L = LINKS.get(uid)
        await _answer_cb(cid)
        if not L:
            await _edit(chat_id, mid, "پیدا نشد.", _main_menu())
            return
        on = is_link_allowed(L)
        used = fmt_bytes(int(L.get("used_bytes") or 0))
        lim = fmt_bytes(int(L.get("limit_bytes") or 0)) if L.get("limit_bytes") else "∞"
        ips = len(unique_ips_for_uuid(uid))
        txt = (
            f"{'🟢' if on else '🔴'} <b>{L.get('label') or uid[:8]}</b>\n"
            f"پروتکل: <code>{L.get('protocol')}</code>\n"
            f"مصرف: {used} / {lim}\n"
            f"IP متصل: {ips}\n"
            f"UUID: <code>{uid}</code>"
        )
        await _edit(chat_id, mid, txt, _detail_kb(uid, on))
        return

    if data.startswith("link:"):
        uid = data.split(":", 1)[1]
        L = LINKS.get(uid)
        await _answer_cb(cid)
        if not L:
            return
        host = _host()
        vless = vless_link_for_link(L, uid, host)
        await _send(chat_id, f"🔗 VLESS:\n<code>{vless}</code>")
        return

    if data.startswith("sub:"):
        uid = data.split(":", 1)[1]
        await _answer_cb(cid)
        host = _host()
        await _send(chat_id, f"📡 ساب:\n<code>https://{host}/sub/{uid}</code>")
        return

    if data.startswith("tog:"):
        uid = data.split(":", 1)[1]
        L = LINKS.get(uid)
        if not L:
            await _answer_cb(cid, "نیست", alert=True)
            return
        new_state = not is_link_allowed(L)
        await set_link_active(uid, new_state)
        await _answer_cb(cid, "روشن شد" if new_state else "خاموش شد")
        on = is_link_allowed(LINKS.get(uid) or {})
        await _edit(
            chat_id,
            mid,
            f"{'🟢' if on else '🔴'} <b>{(LINKS.get(uid) or {}).get('label')}</b>\nوضعیت به‌روز شد.",
            _detail_kb(uid, on),
        )
        return

    if data.startswith("del:"):
        uid = data.split(":", 1)[1]
        await remove_link(uid)
        await _answer_cb(cid, "حذف شد")
        t, kb = _links_page(0)
        await _edit(chat_id, mid, t, kb)
        return

    await _answer_cb(cid)


async def _handle_text(chat_id: int, text: str):
    if not _is_admin(chat_id):
        return
    if text.startswith("/start"):
        await _handle_start(chat_id)
        return
    if text.strip() in ("/cancel", "انصراف"):
        _pending.pop(chat_id, None)
        await _send(chat_id, "لغو شد.", _main_menu())
        return

    st = _pending.get(chat_id)
    if not st:
        await _send(chat_id, "از منو استفاده کنید.", _main_menu())
        return

    step = st["step"]
    data = st["data"]

    if step == "label":
        data["label"] = text.strip()[:40] or f"tg-{int(time.time())%10000}"
        st["step"] = "protocol"
        rows = [[{"text": PROTOCOL_LABELS.get(p, p), "callback_data": f"mproto:{p}"}] for p in list(PROTOCOLS)[:8]]
        rows.append([{"text": "❌ انصراف", "callback_data": "menu"}])
        await _send(chat_id, "پروتکل را انتخاب کنید:", _kb(rows))
        return

    if step == "volume":
        try:
            gb = float(text.replace(",", ".").strip())
        except Exception:
            await _send(chat_id, "عدد معتبر بفرستید (مثلاً 10). 0 = نامحدود")
            return
        data["limit_bytes"] = int(gb * (1024**3)) if gb > 0 else 0
        st["step"] = "days"
        await _send(chat_id, "مدت انقضا به روز؟ (0 = بدون انقضا)")
        return

    if step == "days":
        try:
            days = int(float(text.strip()))
        except Exception:
            await _send(chat_id, "عدد روز را بفرستید.")
            return
        exp = (datetime.now() + timedelta(days=days)).isoformat() if days > 0 else None
        try:
            uid, link = await make_link(
                label=data.get("label", "tg"),
                limit_bytes=int(data.get("limit_bytes") or 0),
                expires_at=exp,
                protocol=data.get("protocol") or DEFAULT_PROTOCOL,
                fingerprint=DEFAULT_FINGERPRINT,
                alpn="http/1.1",
                port=443,
                owner_id=None,
            )
            host = _host()
            vless = vless_link_for_link(link, uid, host)
            sub = f"https://{host}/sub/{uid}"
            _pending.pop(chat_id, None)
            await _send(
                chat_id,
                f"✅ <b>ساخته شد</b>\n"
                f"نام: <code>{link.get('label')}</code>\n"
                f"پروتکل: {link.get('protocol')}\n"
                f"حجم: {fmt_bytes(int(link.get('limit_bytes') or 0)) or '∞'}\n\n"
                f"<code>{vless}</code>\n\n📡 <code>{sub}</code>",
                _detail_kb(uid, True),
            )
        except Exception as e:
            _pending.pop(chat_id, None)
            await _send(chat_id, f"❌ خطا: {e}", _main_menu())
        return


async def _handle_callback_proto(cb: dict):
    """protocol pick during manual wizard"""
    chat_id = cb["message"]["chat"]["id"]
    data = cb.get("data") or ""
    if not data.startswith("mproto:"):
        return False
    if not _is_admin(chat_id):
        return True
    proto = data.split(":", 1)[1]
    st = _pending.get(chat_id)
    if not st:
        await _answer_cb(cb["id"], "منقضی شد", alert=True)
        return True
    st["data"]["protocol"] = proto
    st["step"] = "volume"
    await _answer_cb(cb["id"])
    await _send(chat_id, f"پروتکل: {PROTOCOL_LABELS.get(proto, proto)}\nحجم به GB؟ (0=نامحدود)")
    return True


async def _process_update(upd: dict):
    try:
        if "callback_query" in upd:
            cb = upd["callback_query"]
            if await _handle_callback_proto(cb):
                return
            await _handle_callback(cb)
            return
        msg = upd.get("message") or upd.get("edited_message")
        if not msg:
            return
        chat_id = msg["chat"]["id"]
        text = (msg.get("text") or "").strip()
        if text:
            await _handle_text(chat_id, text)
    except Exception as e:
        logger.exception("telegram update error: %s", e)


async def _poll_loop():
    global _running
    offset = 0
    _running = True
    logger.info("PX Bot polling started")
    while _running:
        try:
            data = await _call(
                "getUpdates",
                offset=offset,
                timeout=25,
                allowed_updates=["message", "callback_query"],
            )
            if not data or not data.get("ok"):
                await asyncio.sleep(2)
                continue
            for upd in data.get("result") or []:
                offset = max(offset, int(upd["update_id"]) + 1)
                await _process_update(upd)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning("poll error: %s", e)
            await asyncio.sleep(3)


async def start_bot_legacy():
    """Called from main startup if token configured."""
    global _poll_task, BOT_TOKEN, API_BASE, ADMIN_IDS
    # reload from TG settings file if present
    tg_file = Path(DATA_DIR) / "telegram_settings.json"
    if tg_file.exists():
        try:
            import json
            conf = json.loads(tg_file.read_text(encoding="utf-8"))
            tok = (conf.get("token") or "").strip()
            if tok:
                BOT_TOKEN = tok
                API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
            ids = conf.get("admin_ids") or conf.get("admin_id") or ""
            if isinstance(ids, list):
                ADMIN_IDS = {int(x) for x in ids if str(x).isdigit()}
            else:
                ADMIN_IDS = {
                    int(x)
                    for x in str(ids).replace(" ", "").split(",")
                    if x.isdigit()
                }
        except Exception as e:
            logger.warning("tg settings load: %s", e)

    if not BOT_TOKEN:
        logger.info("Telegram bot: no token — skipped")
        return
    await _call("setMyCommands", commands=[
        {"command": "start", "description": "منوی اصلی"},
        {"command": "cancel", "description": "لغو عملیات"},
    ])
    if _poll_task and not _poll_task.done():
        return
    _poll_task = asyncio.create_task(_poll_loop())


async def stop_bot():
    global _running, _poll_task, _client
    _running = False
    if _poll_task:
        _poll_task.cancel()
        try:
            await _poll_task
        except Exception:
            pass
    if _client:
        await _client.aclose()
        _client = None


# ─── API سازگار با main.py ───────────────────────────────────

def configure_bot(token: str, admin_ids) -> None:
    global BOT_TOKEN, API_BASE, ADMIN_IDS
    BOT_TOKEN = (token or "").strip()
    API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""
    if isinstance(admin_ids, (list, set, tuple)):
        ADMIN_IDS = {int(x) for x in admin_ids if str(x).isdigit()}
    else:
        ADMIN_IDS = {
            int(x)
            for x in str(admin_ids or "").replace(" ", "").split(",")
            if x.isdigit()
        }
    logger.info("Telegram configure_bot: token=%s admins=%s", bool(BOT_TOKEN), ADMIN_IDS)


async def setup_webhook(url: str = "") -> bool:
    if not BOT_TOKEN:
        return False
    if url:
        r = await _call("setWebhook", url=url, allowed_updates=["message", "callback_query"])
    else:
        r = await _call("deleteWebhook", drop_pending_updates=False)
    ok = bool(r and r.get("ok"))
    logger.info("Telegram webhook setup url=%r ok=%s", url, ok)
    return ok


async def process_update(data: dict):
    await _process_update(data or {})


async def start_bot(mode: str = "polling"):
    """mode: polling | webhook"""
    global _poll_task, _running
    if not BOT_TOKEN:
        # try load from file
        await start_bot_from_disk()
        if not BOT_TOKEN:
            return
    if mode == "webhook":
        _running = False
        if _poll_task and not _poll_task.done():
            _poll_task.cancel()
        logger.info("Telegram bot in webhook mode")
        return
    # polling
    if _poll_task and not _poll_task.done():
        return
    _poll_task = asyncio.create_task(_poll_loop())


async def start_bot_from_disk():
    global BOT_TOKEN, API_BASE, ADMIN_IDS
    tg_file = Path(DATA_DIR) / "telegram_settings.json"
    if not tg_file.exists():
        return
    try:
        import json
        conf = json.loads(tg_file.read_text(encoding="utf-8"))
        tok = (conf.get("token") or "").strip()
        if tok:
            BOT_TOKEN = tok
            API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
        ids = conf.get("admin_ids") or ""
        if isinstance(ids, list):
            ADMIN_IDS = {int(x) for x in ids if str(x).isdigit()}
        else:
            ADMIN_IDS = {
                int(x)
                for x in str(ids).replace(" ", "").split(",")
                if x.isdigit()
            }
    except Exception as e:
        logger.warning("start_bot_from_disk: %s", e)
