#!/usr/bin/env python3
"""Batch-update wholesale and landlord module pages — nav, CTAs, footers."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WHOLESALE_MODULES = [
    "dashboard.html", "customers.html", "products.html", "suppliers.html",
    "categories.html", "orders.html", "invoices.html", "credit-notes.html",
    "accounting.html", "analytics.html", "booking.html", "send-message.html",
    "support.html", "staff.html", "settings.html", "audit-log.html",
]

LANDLORD_MODULES = [
    "landlord/properties.html", "landlord/tenants.html", "landlord/rent-tracker.html",
    "landlord/accounting.html", "landlord/certificates.html", "landlord/viewings.html",
    "landlord/inventory.html",
]

NAV_CSS = """
.nav-links{display:flex;align-items:center;gap:2px;flex-shrink:1;min-width:0}
.nav-link{padding:7px 13px;border-radius:50px;font-size:13px;font-weight:700;color:#374151;transition:all .15s;white-space:nowrap;border:none;background:none;font-family:inherit;cursor:pointer;text-decoration:none}
.nav-link:hover{background:#f1f5f9;color:#0f172a}
.nav-dropdown{position:relative}
.nav-drop-btn{display:inline-flex;align-items:center;gap:5px}
.nav-drop-btn::after{content:'▾';font-size:10px;opacity:.55;transition:transform .2s}
.nav-dropdown:hover .nav-drop-btn::after,.nav-dropdown:focus-within .nav-drop-btn::after{transform:rotate(180deg)}
.nav-drop-panel{display:none;position:absolute;top:calc(100% + 10px);right:0;left:auto;transform:none;min-width:560px;max-width:min(560px,calc(100vw - 24px));background:#fff;border:1px solid #e2e8f0;border-radius:20px;box-shadow:0 28px 70px rgba(15,23,42,.16),0 0 0 1px rgba(255,255,255,.85) inset;padding:18px;grid-template-columns:1fr 1fr;gap:14px;z-index:500}
.nav-dropdown:hover .nav-drop-panel,.nav-dropdown:focus-within .nav-drop-panel{display:grid}
.drop-suite{background:linear-gradient(180deg,#f8fafc 0%,#fff 100%);border:1px solid #eef2f7;border-radius:16px;padding:14px 14px 12px}
.drop-suite.drop-ll{background:linear-gradient(180deg,#f0fdf4 0%,#fff 100%);border-color:#dcfce7}
.drop-head{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:#2563eb;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.drop-head.ll{color:#059669}
.drop-head::before{content:'';width:7px;height:7px;border-radius:50%;background:#2563eb;flex-shrink:0}
.drop-head.ll::before{background:#059669}
.drop-grid{display:grid;grid-template-columns:1fr 1fr;gap:3px}
.drop-mod{display:flex;align-items:center;gap:8px;padding:7px 9px;border-radius:10px;font-size:12px;font-weight:600;color:#475569;text-decoration:none;transition:background .15s,transform .15s,box-shadow .15s}
.drop-mod:hover{background:#fff;color:#0f172a;box-shadow:0 2px 8px rgba(15,23,42,.07);transform:translateY(-1px)}
.drop-mod-ico{font-size:13px;width:18px;text-align:center;flex-shrink:0;line-height:1}
.drop-all{margin-top:8px;padding-top:8px;border-top:1px solid #e2e8f0;font-size:11px;font-weight:800;color:#2563eb;text-decoration:none;display:block}
.drop-all.ll{color:#059669}
.drop-all:hover{text-decoration:underline}
@media(max-width:960px){.nav-links{display:none}}
"""

WHOLESALE_NAV = """<nav>
  <div class="nav-inner">
    <a href="/" class="logo"><img src="/logo.png" alt="ShahoSuite" width="168" height="44" style="height:42px;width:auto;display:block" /></a>
    <div class="nav-links">
      <a href="/wholesale-suite.html" class="nav-link">Wholesale Suite</a>
      <a href="/landlord-suite.html" class="nav-link">Landlord Suite</a>
      <div class="nav-dropdown">
        <button type="button" class="nav-link nav-drop-btn" aria-haspopup="true" aria-expanded="false">Modules</button>
        <div class="nav-drop-panel" role="menu">

          <div class="drop-suite drop-wh">
            <span class="drop-head">Wholesale Suite</span>
            <div class="drop-grid">
              <a href="/dashboard.html" class="drop-mod"><span class="drop-mod-ico">📊</span>Dashboard</a>
              <a href="/customers.html" class="drop-mod"><span class="drop-mod-ico">👥</span>Customers</a>
              <a href="/products.html" class="drop-mod"><span class="drop-mod-ico">📦</span>Products</a>
              <a href="/suppliers.html" class="drop-mod"><span class="drop-mod-ico">🏭</span>Suppliers</a>
              <a href="/orders.html" class="drop-mod"><span class="drop-mod-ico">🛒</span>Orders</a>
              <a href="/invoices.html" class="drop-mod"><span class="drop-mod-ico">🧾</span>Invoices</a>
              <a href="/accounting.html" class="drop-mod"><span class="drop-mod-ico">📕</span>Accounting</a>
              <a href="/analytics.html" class="drop-mod"><span class="drop-mod-ico">📈</span>Analytics</a>
            </div>
            <a href="/wholesale-suite.html" class="drop-all">All wholesale modules →</a>
          </div>
          <div class="drop-suite drop-ll">
            <span class="drop-head ll">Landlord Suite</span>
            <div class="drop-grid">
              <a href="/landlord/properties.html" class="drop-mod"><span class="drop-mod-ico">🏠</span>Properties</a>
              <a href="/landlord/tenants.html" class="drop-mod"><span class="drop-mod-ico">🔑</span>Tenants</a>
              <a href="/landlord/rent-tracker.html" class="drop-mod"><span class="drop-mod-ico">💷</span>Rent Tracker</a>
              <a href="/landlord/certificates.html" class="drop-mod"><span class="drop-mod-ico">✅</span>Docs &amp; Certs</a>
              <a href="/landlord/viewings.html" class="drop-mod"><span class="drop-mod-ico">👁️</span>Viewings</a>
              <a href="/landlord/inventory.html" class="drop-mod"><span class="drop-mod-ico">📋</span>Inventory</a>
              <a href="/landlord/accounting.html" class="drop-mod"><span class="drop-mod-ico">📕</span>Accounting</a>
            </div>
            <a href="/landlord-suite.html" class="drop-all ll">All landlord modules →</a>
          </div>
        </div>
      </div>
      <a href="/pricing.html" class="nav-link">Pricing</a>
      <a href="/articles.html" class="nav-link">Articles</a>
      <a href="/#trust" class="nav-link">Trust</a>
      <a href="mailto:admin@shahosuite.com" class="nav-link">Contact</a>
    </div>
    <div class="nav-btns">
      <a href="https://app.shahosuite.com/login" class="btn-login">Log in</a>
      <a href="https://app.shahosuite.com/register" class="btn-signup">Apply for access</a>
    </div>
  </div>
</nav>"""

LANDLORD_NAV = """<nav>
  <div class="nav-inner">
    <a href="/" class="logo"><img src="/logo.png" alt="ShahoSuite" width="168" height="44" style="height:42px;width:auto;display:block" /></a>
    <div class="nav-links">
      <a href="/wholesale-suite.html" class="nav-link">Wholesale Suite</a>
      <a href="/landlord-suite.html" class="nav-link">Landlord Suite</a>
      <div class="nav-dropdown">
        <button type="button" class="nav-link nav-drop-btn" aria-haspopup="true" aria-expanded="false">Modules</button>
        <div class="nav-drop-panel" role="menu">

          <div class="drop-suite drop-ll">
            <span class="drop-head ll">Landlord Suite</span>
            <div class="drop-grid">
              <a href="/landlord/properties.html" class="drop-mod"><span class="drop-mod-ico">🏠</span>Properties</a>
              <a href="/landlord/tenants.html" class="drop-mod"><span class="drop-mod-ico">🔑</span>Tenants</a>
              <a href="/landlord/rent-tracker.html" class="drop-mod"><span class="drop-mod-ico">💷</span>Rent Tracker</a>
              <a href="/landlord/certificates.html" class="drop-mod"><span class="drop-mod-ico">✅</span>Docs &amp; Certs</a>
              <a href="/landlord/viewings.html" class="drop-mod"><span class="drop-mod-ico">👁️</span>Viewings</a>
              <a href="/landlord/inventory.html" class="drop-mod"><span class="drop-mod-ico">📋</span>Inventory</a>
              <a href="/landlord/accounting.html" class="drop-mod"><span class="drop-mod-ico">📕</span>Accounting</a>
            </div>
            <a href="/landlord-suite.html" class="drop-all ll">All landlord modules →</a>
          </div>
          <div class="drop-suite drop-wh">
            <span class="drop-head">Wholesale Suite</span>
            <div class="drop-grid">
              <a href="/dashboard.html" class="drop-mod"><span class="drop-mod-ico">📊</span>Dashboard</a>
              <a href="/customers.html" class="drop-mod"><span class="drop-mod-ico">👥</span>Customers</a>
              <a href="/products.html" class="drop-mod"><span class="drop-mod-ico">📦</span>Products</a>
              <a href="/suppliers.html" class="drop-mod"><span class="drop-mod-ico">🏭</span>Suppliers</a>
              <a href="/orders.html" class="drop-mod"><span class="drop-mod-ico">🛒</span>Orders</a>
              <a href="/invoices.html" class="drop-mod"><span class="drop-mod-ico">🧾</span>Invoices</a>
              <a href="/accounting.html" class="drop-mod"><span class="drop-mod-ico">📕</span>Accounting</a>
              <a href="/analytics.html" class="drop-mod"><span class="drop-mod-ico">📈</span>Analytics</a>
            </div>
            <a href="/wholesale-suite.html" class="drop-all">All wholesale modules →</a>
          </div>
        </div>
      </div>
      <a href="/pricing.html" class="nav-link">Pricing</a>
      <a href="/articles.html" class="nav-link">Articles</a>
      <a href="/#trust" class="nav-link">Trust</a>
      <a href="mailto:admin@shahosuite.com" class="nav-link">Contact</a>
    </div>
    <div class="nav-btns">
      <a href="https://app.shahosuite.com/login" class="btn-login">Log in</a>
      <a href="https://app.shahosuite.com/register" class="btn-signup">Apply for access</a>
    </div>
  </div>
</nav>"""

FOOTER = """<footer><div class="footer-links">
  <a href="/">Home</a>
  <a href="/wholesale-suite.html">Wholesale Suite</a>
  <a href="/landlord-suite.html">Landlord Suite</a>
  <a href="/pricing.html">Pricing</a>
  <a href="https://app.shahosuite.com/register">Apply for access</a>
  <a href="https://app.shahosuite.com/privacy">Privacy</a>
  <a href="https://app.shahosuite.com/terms">Terms</a>
  <a href="mailto:admin@shahosuite.com">Contact</a>
</div><p>© 2026 Shaho Solutions Limited — Company No. 16017117 — Proprietary software — Portsmouth, UK</p></footer>"""


def global_replacements(text: str) -> str:
    reps = [
        (r"https://shahosuitefrontstorage\.z33\.web\.core\.windows\.net/login", "https://app.shahosuite.com/login"),
        (r">Sign up<", ">Apply for access<"),
        (r">Sign up —", ">Apply for access —"),
        (r"Start a free trial", "Apply for access"),
        (r"Start free trial", "Apply for access"),
        (r"Get started →", "Apply for access →"),
        (r"Sign up as Director →", "Apply for access →"),
        (r'href="/privacy\.html"', 'href="https://app.shahosuite.com/privacy"'),
        (r'href="/terms\.html"', 'href="https://app.shahosuite.com/terms"'),
        (r'href="/index\.html"', 'href="/"'),
        (r'href="/index\.html#features"', 'href="/wholesale-suite.html"'),
        (r'href="/index\.html#trust"', 'href="/#trust"'),
        (r"Sign up — £50/month \+ £15 per staff →", "Apply for access →"),
        (r"Sign up — £50/month →", "Apply for access →"),
        (r"No contracts\. No setup fees\. Cancel any time\.", "We review personally · 14-day guided demo · Response within 1 business day."),
        (r'<div class="section-tag" style="text-align:center;display:block;">Start Today</div>', '<div class="section-tag" style="text-align:center;display:block;">Apply for access</div>'),
    ]
    for old, new in reps:
        text = re.sub(old, new, text)
    return text


def inject_nav_css(text: str) -> str:
    if ".nav-dropdown{" in text:
        return text
    # Insert after first .btn-signup:hover block or before breadcrumb/hero styles
    markers = [".btn-signup:hover {", ".btn-signup:hover{"]
    for m in markers:
        idx = text.find(m)
        if idx == -1:
            continue
        end = text.find("}", idx) + 1
        return text[:end] + NAV_CSS + text[end:]
    # landlord pages
    if ".btn-signup{" in text and ".nav-dropdown{" not in text:
        idx = text.find(".btn-signup{")
        end = text.find("}", idx) + 1
        return text[:end] + NAV_CSS.replace(".nav-link:hover{background:#f1f5f9", ".nav-link:hover{background:#ecfdf5") + text[end:]
    return text


def replace_nav(text: str, nav_html: str) -> str:
    patterns = [
        re.compile(r"<nav[^>]*>.*?</nav>", re.DOTALL),
    ]
    count = 0
    for pat in patterns:
        matches = list(pat.finditer(text))
        if not matches:
            continue
        # Replace first nav only (breadcrumb may be second nav on wholesale pages)
        first = matches[0]
        if "breadcrumb" in first.group():
            continue
        text = text[: first.start()] + nav_html + text[first.end() :]
        count += 1
        break
    return text


def replace_footer(text: str) -> str:
    pat = re.compile(r"<footer[^>]*>.*?</footer>", re.DOTALL | re.IGNORECASE)
    m = pat.search(text)
    if m:
        return text[: m.start()] + FOOTER + text[m.end() :]
    return text


def fix_landlord_breadcrumb(text: str) -> str:
    text = text.replace('href="/index.html#features"', 'href="/landlord-suite.html"')
    return text


def process(path: Path, nav_html: str, is_landlord: bool = False) -> bool:
    if not path.exists():
        print(f"  skip missing: {path}")
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    text = global_replacements(text)
    text = inject_nav_css(text)
    text = replace_nav(text, nav_html)
    text = replace_footer(text)
    if is_landlord:
        text = fix_landlord_breadcrumb(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  updated: {path.relative_to(ROOT)}")
        return True
    print(f"  unchanged: {path.relative_to(ROOT)}")
    return False


def main():
    n = 0
    print("Wholesale modules:")
    for f in WHOLESALE_MODULES:
        if process(ROOT / f, WHOLESALE_NAV):
            n += 1
    print("Landlord modules:")
    for f in LANDLORD_MODULES:
        if process(ROOT / f, LANDLORD_NAV, is_landlord=True):
            n += 1
    print(f"Done — {n} files updated.")


if __name__ == "__main__":
    main()
