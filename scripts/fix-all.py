#!/usr/bin/env python3
"""
Three-part fix:
  1. Unify all inner page Modules dropdowns → homepage drop-col style
  2. Fix module page hero mockup blur so dark sidebar shows through
  3. Clean homepage ticker (remove duplicate / overlapping items)
"""
import re
from pathlib import Path

ROOT = Path('/Users/macbookpro/ShahoSuite-Wbsite')

# ─────────────────────────────────────────────────────────────────
# 1. DROPDOWN FIX
# ─────────────────────────────────────────────────────────────────

# Old CSS block that lives on inner pages (card-style dropdown)
OLD_DROP_CSS_RE = re.compile(
    r'\.nav-drop-panel\{display:none;position:absolute;top:calc\(100% \+ 10px\);right:0;left:auto.*?\.drop-all:hover\{text-decoration:underline\}',
    re.DOTALL,
)

NEW_DROP_CSS = (
    '.nav-drop-panel{display:none;position:absolute;top:calc(100% + 8px);left:50%;'
    'transform:translateX(-50%);min-width:520px;background:#fff;border:1px solid #e2e8f0;'
    'border-radius:16px;box-shadow:0 20px 50px rgba(15,23,42,.12);'
    'padding:16px 18px;grid-template-columns:1fr 1fr;gap:20px;z-index:300}\n'
    '.nav-dropdown:hover .nav-drop-panel,.nav-dropdown:focus-within .nav-drop-panel{display:grid}\n'
    '.drop-head{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:.12em;'
    'color:#2563eb;display:block;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #f1f5f9}\n'
    '.drop-head.ll{color:#059669}\n'
    '.drop-col a{display:block;font-size:12px;font-weight:600;color:#475569;padding:5px 0;transition:color .15s}\n'
    '.drop-col a:hover{color:#0f172a}'
)

NEW_DROP_PANEL = '''\
<div class="nav-drop-panel">
          <div class="drop-col">
            <span class="drop-head">Wholesale Suite</span>
            <a href="/dashboard.html">Dashboard</a>
            <a href="/customers.html">Customers</a>
            <a href="/products.html">Products</a>
            <a href="/suppliers.html">Suppliers</a>
            <a href="/orders.html">Orders</a>
            <a href="/invoices.html">Invoices</a>
            <a href="/accounting.html">Accounting</a>
            <a href="/analytics.html">Analytics</a>
            <a href="/wholesale-suite.html">All wholesale modules →</a>
          </div>
          <div class="drop-col">
            <span class="drop-head ll">Landlord Suite</span>
            <a href="/landlord/properties.html">Properties</a>
            <a href="/landlord/tenants.html">Tenants</a>
            <a href="/landlord/rent-tracker.html">Rent Tracker</a>
            <a href="/landlord/certificates.html">Docs &amp; Certs</a>
            <a href="/landlord/viewings.html">Viewings</a>
            <a href="/landlord/inventory.html">Inventory</a>
            <a href="/landlord/accounting.html">Accounting</a>
            <a href="/landlord-suite.html">All landlord modules →</a>
          </div>
        </div>'''


def find_drop_panel(text):
    """Return (start, end) indices of the nav-drop-panel div, or (-1,-1)."""
    marker = '<div class="nav-drop-panel"'
    start = text.find(marker)
    if start == -1:
        return -1, -1
    # Walk forward counting div depth
    tag_end = text.index('>', start) + 1
    depth = 1
    pos = tag_end
    while pos < len(text) and depth > 0:
        next_open = text.find('<div', pos)
        next_close = text.find('</div>', pos)
        if next_open == -1 and next_close == -1:
            break
        if next_open != -1 and (next_close == -1 or next_open < next_close):
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                return start, pos
    return -1, -1


def fix_dropdown(text):
    """Replace card-style dropdown CSS + HTML with homepage drop-col style."""
    changed = False

    # 1a. Replace CSS
    new_text, n = OLD_DROP_CSS_RE.subn(NEW_DROP_CSS, text)
    if n:
        text = new_text
        changed = True

    # 1b. Replace HTML panel (only if it contains old card-style markup)
    if 'drop-suite' in text or ('drop-mod' in text and 'drop-col' not in text):
        s, e = find_drop_panel(text)
        if s != -1:
            text = text[:s] + NEW_DROP_PANEL + text[e:]
            changed = True

    # 1c. Fix Modules button text (add ▾ to match homepage)
    text = text.replace(
        '" aria-haspopup="true" aria-expanded="false">Modules</button>',
        '" aria-haspopup="true">Modules ▾</button>',
    )
    # Also handle variants without aria-expanded
    text = text.replace(
        '" aria-haspopup="true">Modules</button>',
        '" aria-haspopup="true">Modules ▾</button>',
    )

    return text, changed


# ─────────────────────────────────────────────────────────────────
# 2. HERO MOCKUP FIX — expose dark sidebar through blur
# ─────────────────────────────────────────────────────────────────

OLD_BLUR_CSS = (
    '  position: absolute; inset: 0; z-index: 3;\n'
    '  background: rgba(255,255,255,0.52);\n'
    '  backdrop-filter: blur(7px);\n'
    '  -webkit-backdrop-filter: blur(7px);\n'
)

NEW_BLUR_CSS = (
    '  position: absolute; top: 0; right: 0; bottom: 0; left: 165px; z-index: 3;\n'
    '  background: rgba(255,255,255,0.35);\n'
    '  backdrop-filter: blur(5px);\n'
    '  -webkit-backdrop-filter: blur(5px);\n'
)


FROST_OVERLAY_RE = re.compile(
    r'\.frost-overlay\s*\{[^}]*?position\s*:\s*absolute\s*;[^}]*?inset\s*:\s*0\s*;[^}]*?\}',
    re.DOTALL,
)

FROST_OVERLAY_REPLACE = (
    '.frost-overlay { position: absolute; top: 0; right: 0; bottom: 0; left: 168px; '
    'z-index: 3; background: rgba(255,255,255,0.35); '
    'backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); pointer-events: none; }'
)


def fix_mockup_blur(text):
    """Narrow blur overlay to skip the sidebar column."""
    changed = False
    if OLD_BLUR_CSS in text:
        text = text.replace(OLD_BLUR_CSS, NEW_BLUR_CSS)
        changed = True
    new_text, n = FROST_OVERLAY_RE.subn(FROST_OVERLAY_REPLACE, text)
    if n:
        text = new_text
        changed = True
    return text, changed


# ─────────────────────────────────────────────────────────────────
# 3. HOMEPAGE TICKER — replace with 9 distinct, non-overlapping items
# ─────────────────────────────────────────────────────────────────

TICKER_SECTION_RE = re.compile(
    r'(<!-- ══ TICKER ══ -->.*?<div class="t-track">).*?(</div>\s*</div>\s*</div>)',
    re.DOTALL,
)

NEW_TICKER_ITEMS = """\n      <span class="ti">💡 <strong>CRM + ERP Operating System</strong> — one UK platform</span><span class="ts">·</span>
      <span class="ti">🇬🇧 <strong>Microsoft Azure UK</strong> — your data stays in Britain</span><span class="ts">·</span>
      <span class="ti">🛍️ <strong>Wholesale Suite</strong> — cash &amp; carry, grocery, B2B wholesale</span><span class="ts">·</span>
      <span class="ti">🏘️ <strong>Landlord Suite</strong> — property, lettings and compliance</span><span class="ts">·</span>
      <span class="ti">🔒 <strong>Apply for access</strong> — reviewed within one working day</span><span class="ts">·</span>
      <span class="ti">📦 <strong>Stock, orders &amp; invoices</strong> — complete trade management</span><span class="ts">·</span>
      <span class="ti">💷 <strong>Rent, arrears &amp; certs</strong> — landlord finance in one place</span><span class="ts">·</span>
      <span class="ti">🧑‍💼 <strong>Role-based staff access</strong> — audit trail, zero data risk</span><span class="ts">·</span>
      <span class="ti">⚡ <strong>Minimum clicks · Smart automation · Real autonomy</strong></span><span class="ts">·</span>
      <!-- duplicate for seamless loop -->
      <span class="ti">💡 <strong>CRM + ERP Operating System</strong> — one UK platform</span><span class="ts">·</span>
      <span class="ti">🇬🇧 <strong>Microsoft Azure UK</strong> — your data stays in Britain</span><span class="ts">·</span>
      <span class="ti">🛍️ <strong>Wholesale Suite</strong> — cash &amp; carry, grocery, B2B wholesale</span><span class="ts">·</span>
      <span class="ti">🏘️ <strong>Landlord Suite</strong> — property, lettings and compliance</span><span class="ts">·</span>
      <span class="ti">🔒 <strong>Apply for access</strong> — reviewed within one working day</span><span class="ts">·</span>
      <span class="ti">📦 <strong>Stock, orders &amp; invoices</strong> — complete trade management</span><span class="ts">·</span>
      <span class="ti">💷 <strong>Rent, arrears &amp; certs</strong> — landlord finance in one place</span><span class="ts">·</span>
      <span class="ti">🧑‍💼 <strong>Role-based staff access</strong> — audit trail, zero data risk</span><span class="ts">·</span>
      <span class="ti">⚡ <strong>Minimum clicks · Smart automation · Real autonomy</strong></span><span class="ts">·</span>\n    """


def fix_ticker(text):
    m = TICKER_SECTION_RE.search(text)
    if not m:
        return text, False
    new_text = text[:m.start(1)] + m.group(1) + NEW_TICKER_ITEMS + m.group(2) + text[m.end(2):]
    return new_text, True


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

def process_file(path: Path, is_homepage=False):
    original = path.read_text(encoding='utf-8')
    text = original
    actions = []

    if is_homepage:
        text, ok = fix_ticker(text)
        if ok:
            actions.append('ticker')
    else:
        # Dropdown fix for all non-homepage pages
        text, ok = fix_dropdown(text)
        if ok:
            actions.append('dropdown')

        # Mockup blur fix for pages that have app-body-wrap::after
        text, ok = fix_mockup_blur(text)
        if ok:
            actions.append('mockup-blur')

    if text != original:
        path.write_text(text, encoding='utf-8')
        print(f'  ✓ {path.relative_to(ROOT)}  [{", ".join(actions)}]')
    else:
        if actions or is_homepage:
            print(f'  – {path.relative_to(ROOT)}  (no change)')


all_html = list(ROOT.glob('**/*.html'))
homepage = ROOT / 'index.html'

print('=== fix-all.py ===\n')
print('── homepage ──')
process_file(homepage, is_homepage=True)

print('\n── inner pages ──')
for p in sorted(all_html):
    if p == homepage:
        continue
    # Skip redirect pages (they have noindex meta and minimal HTML)
    content = p.read_text(encoding='utf-8')
    if '<meta name="robots" content="noindex' in content:
        continue
    process_file(p)

print('\nDone.')
