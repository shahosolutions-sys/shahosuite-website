#!/usr/bin/env python3
"""Stage 2 — standardise trust, legal, local SEO pages; redirect legacy URLs."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "update_module_pages", ROOT / "scripts" / "update-module-pages.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

FOOTER = _mod.FOOTER
WHOLESALE_NAV = _mod.WHOLESALE_NAV
global_replacements = _mod.global_replacements
inject_nav_css = _mod.inject_nav_css
replace_footer = _mod.replace_footer
replace_nav = _mod.replace_nav

TRUST_NAV = WHOLESALE_NAV.replace(
    '<a href="/#trust" class="nav-link">Trust</a>',
    '<a href="/security.html" class="nav-link">Trust</a>',
)

TRUST_PAGES = [
    "security.html",
    "founder.html",
    "gdpr.html",
    "portsmouth-warehouses-grocery-operations.html",
    "london-business-operating-system.html",
]

REDIRECTS = {
    "Invoice.html": ("/", "Redirecting to ShahoSuite"),
    "landlord.html": ("/landlord-suite.html", "Redirecting to Landlord Suite"),
    "beauty-salon-suite.html": ("/wholesale-suite.html", "Redirecting to Wholesale Suite"),
    "privacy.html": ("https://app.shahosuite.com/privacy", "Redirecting to Privacy Policy"),
    "terms.html": ("https://app.shahosuite.com/terms", "Redirecting to Terms of Service"),
}


def extra_replacements(text: str) -> str:
    reps = [
        (r"https://shahosuitefrontstorage\.z33\.web\.core\.windows\.net/login", "https://app.shahosuite.com/login"),
        (r'href="/index\.html"', 'href="/"'),
        (r">Sign up<", ">Apply for access<"),
        (r">Sign up —", ">Apply for access —"),
        (r">Get started<", ">Apply for access<"),
        (r">Get Started —", ">Apply for access —"),
        (r'href="/privacy\.html"', 'href="https://app.shahosuite.com/privacy"'),
        (r'href="/terms\.html"', 'href="https://app.shahosuite.com/terms"'),
        (r"Privacy Policy", "Privacy"),
        (r"Terms of Service", "Terms"),
        (r"/beauty-salon-suite\.html", "/wholesale-suite.html"),
    ]
    for old, new in reps:
        text = re.sub(old, new, text)
    return text


def fix_cta_copy(text: str) -> str:
    text = text.replace(
        "All included in £50/month.",
        "Apply for access — we review personally, respond within one business day, and set you up with a 14-day guided demo.",
    )
    text = text.replace(
        "Microsoft Azure hosting · AES-256 encryption · UK data centres · GDPR compliant · Full audit log · Role-based access.",
        "UK CRM + ERP Business Management Operating System · Microsoft Azure UK · Apply-only onboarding with personal review.",
    )
    return text


def inject_page_margin(text: str) -> str:
    """Ensure fixed nav pages have top padding when nav-links added."""
    if "margin-top:68px" not in text and "margin-top: 68px" not in text:
        text = text.replace(
            ".page-wrap{max-width:",
            ".page-wrap{margin-top:68px;max-width:",
        )
        text = text.replace(
            ".page-wrap { max-width:",
            ".page-wrap { margin-top: 68px; max-width:",
        )
        text = text.replace(
            ".main-wrap { max-width:",
            ".main-wrap { margin-top: 68px; max-width:",
        )
        text = text.replace(
            ".hero { padding: 120px",
            ".hero { padding: 120px",
        )
    return text


def make_redirect(target: str, title: str) -> str:
    canonical = target if target.startswith("http") else f"https://www.shahosuite.com{target}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0;url={target}">
<title>{title}</title>
</head>
<body>
<p>Redirecting… <a href="{target}">Continue</a></p>
</body>
</html>
"""


def process_trust_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = global_replacements(text)
    text = extra_replacements(text)
    text = fix_cta_copy(text)
    text = inject_nav_css(text)
    text = replace_nav(text, TRUST_NAV)
    text = replace_footer(text)
    text = inject_page_margin(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  updated: {path.relative_to(ROOT)}")
        return True
    print(f"  unchanged: {path.relative_to(ROOT)}")
    return False


def write_redirects() -> int:
    n = 0
    for name, (target, title) in REDIRECTS.items():
        path = ROOT / name
        content = make_redirect(target, title)
        if path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            print(f"  redirect: {name} → {target}")
            n += 1
    return n


def fix_certificates_get_started() -> bool:
    path = ROOT / "landlord/certificates.html"
    text = path.read_text(encoding="utf-8")
    new = global_replacements(extra_replacements(text))
    if new != text:
        path.write_text(new, encoding="utf-8")
        print("  updated: landlord/certificates.html (CTA text)")
        return True
    return False


def main():
    n = 0
    print("Trust & local SEO pages:")
    for name in TRUST_PAGES:
        if process_trust_page(ROOT / name):
            n += 1
    print("Legacy redirects:")
    n += write_redirects()
    if fix_certificates_get_started():
        n += 1
    print(f"Done — {n} changes.")


if __name__ == "__main__":
    main()
