#!/usr/bin/env python3
"""Patch site UI: modules dropdown, hero backgrounds, articles nav, duplicate guards."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "update_module_pages", ROOT / "scripts" / "update-module-pages.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

WHOLESALE_MODULES = _mod.WHOLESALE_MODULES
LANDLORD_MODULES = _mod.LANDLORD_MODULES
FOOTER = _mod.FOOTER
global_replacements = _mod.global_replacements

# ── Improved modules dropdown CSS ──
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

WHOLESALE_DROP = """
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
          </div>"""

LANDLORD_DROP = """
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
          </div>"""


def build_nav(trust_href="/#trust", landlord_first=False):
    wh, ll = WHOLESALE_DROP, LANDLORD_DROP
    cols = (ll + wh) if landlord_first else (wh + ll)
    return f"""<nav>
  <div class="nav-inner">
    <a href="/" class="logo"><img src="/logo.png" alt="ShahoSuite" width="168" height="44" style="height:42px;width:auto;display:block" /></a>
    <div class="nav-links">
      <a href="/wholesale-suite.html" class="nav-link">Wholesale Suite</a>
      <a href="/landlord-suite.html" class="nav-link">Landlord Suite</a>
      <div class="nav-dropdown">
        <button type="button" class="nav-link nav-drop-btn" aria-haspopup="true" aria-expanded="false">Modules</button>
        <div class="nav-drop-panel" role="menu">
{cols}
        </div>
      </div>
      <a href="/pricing.html" class="nav-link">Pricing</a>
      <a href="/articles.html" class="nav-link">Articles</a>
      <a href="{trust_href}" class="nav-link">Trust</a>
      <a href="mailto:admin@shahosuite.com" class="nav-link">Contact</a>
    </div>
    <div class="nav-btns">
      <a href="https://app.shahosuite.com/login" class="btn-login">Log in</a>
      <a href="https://app.shahosuite.com/register" class="btn-signup">Apply for access</a>
    </div>
  </div>
</nav>"""


STANDARD_NAV = build_nav()
LANDLORD_NAV = build_nav(landlord_first=True)
TRUST_NAV = build_nav(trust_href="/security.html")

FOOTER_V2 = FOOTER.replace(
    '<a href="/pricing.html">Pricing</a>',
    '<a href="/pricing.html">Pricing</a>\n  <a href="/articles.html">Articles</a>',
)

HERO_CSS = """
#hero-canvas{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:.44}
.hero::before{content:'';position:absolute;inset:0;z-index:0;pointer-events:none;background:radial-gradient(ellipse 72% 58% at 50% -8%,var(--hero-glow,rgba(59,130,246,.12)),transparent 70%)}
.hero-inner,.hero>.module-badge,.hero>h1,.hero>.hero-sub,.hero>.trust-row,.hero>.mockup-outer,.hero>.hero-ctas{position:relative;z-index:1}
"""

HERO_SCRIPT = '<script src="/assets/hero-bg.js" defer></script>'

SITE_PAGES = [
    "index.html", "pricing.html", "wholesale-suite.html", "landlord-suite.html",
    "security.html", "founder.html", "gdpr.html", "articles.html",
    "portsmouth-warehouses-grocery-operations.html", "london-business-operating-system.html",
] + WHOLESALE_MODULES + LANDLORD_MODULES

OLD_NAV_CSS_PAT = re.compile(
    r"\.nav-links\{display:flex.*?@media\(max-width:880px\)\{\.nav-links\{display:none\}\}\s*",
    re.DOTALL,
)
OLD_NAV_CSS_PAT2 = re.compile(
    r"\.nav-links\{display:flex.*?@media\(max-width:960px\)\{\.nav-links\{display:none\}\}\s*",
    re.DOTALL,
)


def replace_nav_css(text: str) -> str:
    if ".drop-mod{" in text:
        return text
    for pat in (OLD_NAV_CSS_PAT, OLD_NAV_CSS_PAT2):
        if pat.search(text):
            return pat.sub(NAV_CSS, text, count=1)
    # index.html uses slightly different nav css block
    idx = text.find(".nav-dropdown{position:relative}")
    if idx != -1 and ".drop-mod{" not in text:
        end = text.find("@media(max-width:640px)", idx)
        if end == -1:
            end = text.find(".nav-btns{", idx)
        if end != -1:
            return text[:idx] + NAV_CSS.strip() + "\n" + text[end:]
    # Pages with new nav HTML but no dropdown CSS at all
    if "drop-mod" in text and ".nav-links{" not in text:
        for m in (".btn-signup:active {", ".btn-signup:active{", ".btn-signup:hover {", ".btn-signup:hover{", ".btn-signup {", ".btn-signup{"):
            if m in text:
                end = text.find("}", text.find(m)) + 1
                return text[:end] + NAV_CSS + text[end:]
    return text


def replace_nav_block(text: str, nav_html: str) -> str:
    pat = re.compile(r"<nav[^>]*>.*?</nav>", re.DOTALL)
    m = pat.search(text)
    if not m or "breadcrumb" in m.group():
        return text
    return text[: m.start()] + nav_html + text[m.end() :]


def inject_hero_css(text: str, variant: str = "wholesale") -> str:
    glow = "rgba(16,185,129,.11)" if variant == "landlord" else "rgba(59,130,246,.11)"
    if "#hero-canvas{" not in text:
        marker = ".hero {"
        if marker not in text:
            marker = ".hero{"
        if marker in text:
            text = text.replace(marker, f":root{{--hero-glow:{glow};}}\n{marker}", 1)
            insert_at = text.find(marker) + len(marker)
            text = text[:insert_at] + " position:relative;overflow:hidden;" + text[insert_at:]
        css_block = HERO_CSS.replace("rgba(59,130,246,.12)", glow)
        if "#hero-canvas{" not in text:
            style_end = text.rfind("</style>")
            if style_end != -1:
                text = text[:style_end] + css_block + text[style_end:]
    return text


def inject_hero_canvas(text: str, variant: str) -> str:
    if 'id="hero-canvas"' in text:
        if f'data-variant="{variant}"' not in text:
            text = text.replace('id="hero-canvas"', f'id="hero-canvas" data-variant="{variant}"', 1)
        return text
    pat = re.compile(r'(<section class="hero">)\s*', re.IGNORECASE)
    m = pat.search(text)
    if m:
        canvas = f'{m.group(1)}\n  <canvas id="hero-canvas" data-variant="{variant}" aria-hidden="true"></canvas>\n  '
        return text[: m.start()] + canvas + text[m.end() :]
    return text


def inject_hero_script(text: str) -> str:
    if "hero-bg.js" in text:
        return text
    if "</body>" in text:
        return text.replace("</body>", HERO_SCRIPT + "\n</body>", 1)
    return text


def replace_footer(text: str) -> str:
    pat = re.compile(r"<footer[^>]*>.*?</footer>", re.DOTALL | re.IGNORECASE)
    m = pat.search(text)
    if m:
        return text[: m.start()] + FOOTER_V2 + text[m.end() :]
    return text


def patch_page(path: Path, nav_html: str, hero_variant=None) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    orig = text
    text = global_replacements(text)
    text = replace_nav_css(text)
    text = replace_nav_block(text, nav_html)
    text = replace_footer(text)
    if hero_variant:
        text = inject_hero_css(text, hero_variant)
        text = inject_hero_canvas(text, hero_variant)
        text = inject_hero_script(text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"  patched: {path.relative_to(ROOT)}")
        return True
    return False


def noindex_demo():
    path = ROOT / "suite-landlord-demo.html"
    text = path.read_text(encoding="utf-8")
    if "noindex" in text:
        return
    text = text.replace(
        "<head>",
        '<head>\n<meta name="robots" content="noindex, nofollow" />\n<link rel="canonical" href="https://www.shahosuite.com/landlord-suite.html" />',
        1,
    )
    path.write_text(text, encoding="utf-8")
    print("  noindex: suite-landlord-demo.html")


def patch_index_nav_css(text: str) -> str:
    """Update index.html nav dropdown to match new design."""
    old = """.nav-drop-panel{display:none;position:absolute;top:calc(100% + 8px);left:50%;transform:translateX(-50%);min-width:520px;background:#fff;border:1px solid #e2e8f0;border-radius:16px;box-shadow:0 20px 50px rgba(15,23,42,.12);padding:16px 18px;grid-template-columns:1fr 1fr;gap:20px;z-index:300}
.nav-dropdown:hover .nav-drop-panel,.nav-dropdown:focus-within .nav-drop-panel{display:grid}
.drop-head{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:#2563eb;display:block;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #f1f5f9}
.drop-head.ll{color:#059669}
.drop-col a{display:block;font-size:12px;font-weight:600;color:#475569;padding:5px 0;transition:color .15s}
.drop-col a:hover{color:#0f172a}"""
    if old in text:
        text = text.replace(old, NAV_CSS.strip().split(".nav-links{")[1].split("@media")[0].strip())
    return text


def patch_index():
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    orig = text
    # Replace nav dropdown panel content
    text = replace_nav_css(text)
    nav = build_nav()
    text = replace_nav_block(text, nav)
    # Footer articles link
    if "/articles.html" not in text:
        text = text.replace(
            '<a href="/pricing.html">Pricing</a>',
            '<a href="/pricing.html">Pricing</a>\n    <a href="/articles.html">Articles</a>',
            1,
        )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("  patched: index.html")


def main():
    n = 0
    print("Module pages (wholesale):")
    for f in WHOLESALE_MODULES:
        if patch_page(ROOT / f, STANDARD_NAV, "wholesale"):
            n += 1
    print("Module pages (landlord):")
    for f in LANDLORD_MODULES:
        if patch_page(ROOT / f, LANDLORD_NAV, "landlord"):
            n += 1
    print("Site pages:")
    site_nav = {
        "index.html": None,  # handled separately
        "pricing.html": (STANDARD_NAV, "neutral"),
        "wholesale-suite.html": (STANDARD_NAV, "wholesale"),
        "landlord-suite.html": (LANDLORD_NAV, "landlord"),
        "security.html": (TRUST_NAV, "neutral"),
        "founder.html": (TRUST_NAV, "neutral"),
        "gdpr.html": (TRUST_NAV, "neutral"),
        "articles.html": (STANDARD_NAV, "neutral"),
        "portsmouth-warehouses-grocery-operations.html": (STANDARD_NAV, "wholesale"),
        "london-business-operating-system.html": (STANDARD_NAV, "neutral"),
    }
    patch_index()
    n += 1
    for name, cfg in site_nav.items():
        if name == "index.html" or cfg is None:
            continue
        nav, variant = cfg
        if patch_page(ROOT / name, nav, variant):
            n += 1
    noindex_demo()
    # Sync update-module-pages.py nav for future runs
    sync_script_nav()
    print(f"Done — {n} pages patched.")


def sync_script_nav():
    """Keep update-module-pages.py in sync for future batch updates."""
    path = ROOT / "scripts" / "update-module-pages.py"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'NAV_CSS = """.*?"""',
        'NAV_CSS = """\n' + NAV_CSS.strip() + '\n"""',
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'WHOLESALE_NAV = """.*?"""',
        'WHOLESALE_NAV = """' + build_nav() + '"""',
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'LANDLORD_NAV = """.*?"""',
        'LANDLORD_NAV = """' + build_nav(landlord_first=True) + '"""',
        text,
        count=1,
        flags=re.DOTALL,
    )
    path.write_text(text, encoding="utf-8")
    print("  synced: scripts/update-module-pages.py")


if __name__ == "__main__":
    main()
