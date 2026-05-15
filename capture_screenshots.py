"""Capture screenshots of pymempresas.com at various viewports."""
import sys
sys.path.insert(0, r'C:\Users\aviei\AppData\Roaming\Python\Python312\site-packages')

from playwright.sync_api import sync_playwright
import os

BASE_URL = "https://pymempresas.com"
OUTPUT_DIR = r"C:\Users\aviei\Documents\Pymempresas\pymempresas-web\screenshots"

viewports = {
    "desktop-1920": (1920, 1080),
    "laptop-1366": (1366, 768),
    "tablet-768": (768, 1024),
    "mobile-375": (375, 812),
}

# Only full-page for desktop, above-fold for mobile
pages_to_capture = {
    "homepage": "/",
    "seo-local-gijon": "/seo-local-gijon/",
    "diseno-web-gijon": "/diseno-web-gijon/",
    "consultoria": "/consultoria/",
    "contacto": "/contacto/",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    for page_name, path in pages_to_capture.items():
        url = BASE_URL + path
        print(f"\n=== Capturing {page_name} ({url}) ===")

        for device, (width, height) in viewports.items():
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
            )
            page = context.new_page()

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                # Extra wait for fonts and images
                page.wait_for_timeout(2000)

                # Full-page screenshot for all
                full_path = os.path.join(OUTPUT_DIR, f"{page_name}_{device}_full.png")
                page.screenshot(path=full_path, full_page=True)

                # Above-fold screenshot (only viewport)
                fold_path = os.path.join(OUTPUT_DIR, f"{page_name}_{device}_fold.png")
                page.screenshot(path=fold_path, full_page=False)

                # Check for horizontal scroll on mobile
                if width <= 768:
                    scroll_width = page.evaluate("document.documentElement.scrollWidth")
                    viewport_width = page.evaluate("window.innerWidth")
                    overflow_x = scroll_width - viewport_width
                    print(f"  [{device}] ScrollWidth: {scroll_width}px, Viewport: {viewport_width}px, OverflowX: {overflow_x}px {'*** OVERFLOW ***' if overflow_x > 10 else ''}")

                # Get some metrics
                h1_count = page.evaluate("document.querySelectorAll('h1').length")
                h1_texts = page.evaluate("Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim())")
                print(f"  [{device}] H1s: {h1_texts}")

                # Check cookie banner
                has_cookie = page.evaluate("document.querySelector('[class*=\"cookie\" i], [class*=\"Cookie\" i], [id*=\"cookie\" i], [id*=\"Cookie\" i]') !== null")
                print(f"  [{device}] Cookie banner present: {has_cookie}")

                # Check mobile menu
                if width <= 768:
                    has_hamburger = page.evaluate("""
                        () => {
                            const btns = document.querySelectorAll('button, a');
                            for (const btn of btns) {
                                const html = btn.innerHTML.toLowerCase();
                                if (html.includes('menu') || html.includes('hamburger') || html.includes('navbar-toggle') ||
                                    html.includes('ti-menu') || html.includes('ti-align') || html.includes('bars') ||
                                    btn.classList.toString().toLowerCase().includes('hamburger') ||
                                    btn.classList.toString().toLowerCase().includes('menu-toggle') ||
                                    btn.classList.toString().toLowerCase().includes('navbar-toggle') ||
                                    btn.getAttribute('aria-label')?.toLowerCase().includes('menu'))
                                    return true;
                            }
                            return false;
                        }
                    """)
                    print(f"  [{device}] Hamburger menu found: {has_hamburger}")

                # Check hero content above fold
                page.evaluate("window.scrollTo(0, 0)")
                fold_text = page.evaluate("""
                    () => {
                        const vp = window.innerHeight;
                        const els = [];
                        document.querySelectorAll('h1, h2, p, a, button').forEach(el => {
                            const rect = el.getBoundingClientRect();
                            if (rect.top < vp && rect.bottom > 0) {
                                const text = el.textContent.trim().substring(0, 80);
                                const tag = el.tagName;
                                els.push({tag, text, top: Math.round(rect.top), bottom: Math.round(rect.bottom)});
                            }
                        });
                        return els.slice(0, 30);
                    }
                """)
                print(f"  [{device}] Above-fold elements:")
                for el in fold_text:
                    print(f"    <{el['tag']}> top={el['top']} bot={el['bottom']}: {el['text']}")

            except Exception as e:
                print(f"  [{device}] ERROR: {e}")
            finally:
                context.close()

    browser.close()

print("\n=== All screenshots captured ===")
