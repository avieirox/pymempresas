"""Final targeted checks."""
import sys
sys.path.insert(0, r'C:\Users\aviei\AppData\Roaming\Python\Python312\site-packages')

from playwright.sync_api import sync_playwright

BASE_URL = "https://pymempresas.com"

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ====== Cookie banner clickability check ======
    print("=" * 60)
    print("COOKIE BANNER - INTERACTION TEST (mobile)")
    print("=" * 60)

    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    # Check if hamburger is clickable before dismissing cookie
    clickable_test = page.evaluate("""
        () => {
            const r = {};
            const cookie = document.querySelector('[class*="cookie" i], [class*="Cookie" i], [class*="consent" i]');
            const hamburger = document.getElementById('mobile-menu-btn');

            if (cookie) {
                r.cookieZ = window.getComputedStyle(cookie).zIndex;
                r.cookiePosition = window.getComputedStyle(cookie).position;
            }
            if (hamburger) {
                r.hamburgerZ = window.getComputedStyle(hamburger).zIndex;
                r.hamburgerPosition = window.getComputedStyle(hamburger).position;
                r.hamburgerPointerEvents = window.getComputedStyle(hamburger).pointerEvents;
            }

            // Check cookie overlay dimensions
            const overlay = cookie?.querySelector('[class*="overlay" i]') || cookie;
            if (overlay) {
                const rect = overlay.getBoundingClientRect();
                r.overlayRect = {
                    top: Math.round(rect.top),
                    left: Math.round(rect.left),
                    bottom: Math.round(rect.bottom),
                    right: Math.round(rect.right),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                };
                r.coversEverything = rect.top <= 0 && rect.left <= 0 && rect.bottom >= window.innerHeight && rect.right >= window.innerWidth;
            }

            return r;
        }
    """)
    print(f"Cookie z-index: {clickable_test.get('cookieZ')}")
    print(f"Hamburger z-index: {clickable_test.get('hamburgerZ')}")
    print(f"Hamburger pointer-events: {clickable_test.get('hamburgerPointerEvents')}")
    print(f"Overlay covers everything: {clickable_test.get('overlayRect')}")

    # Try clicking hamburger BEFORE dismissing cookie
    try:
        hamburger = page.locator('#mobile-menu-btn')
        is_visible_before = hamburger.is_visible()
        print(f"Hamburger visible: {is_visible_before}")

        # Check if the cookie overlay is intercepting clicks
        is_enabled = hamburger.is_enabled()
        print(f"Hamburger enabled: {is_enabled}")

        # Try to click (may hit cookie overlay instead)
        hamburger.click(timeout=1000)
        page.wait_for_timeout(500)
        print("Hamburger clicked successfully (before cookie dismiss)")

        # Check if menu appeared
        menu_visible = page.evaluate("document.getElementById('mobile-menu')?.classList.contains('hidden') === false")
        print(f"Mobile menu appeared: {menu_visible}")
    except Exception as e:
        print(f"Hamburger click FAILED (cookie blocking): {e}")

    # Now dismiss cookie and try again
    try:
        page.locator('#cookie-reject-all').click(timeout=2000)
        page.wait_for_timeout(500)
        print("\nCookie banner dismissed")
    except Exception as e:
        print(f"Could not click reject: {e}")
        try:
            page.locator('#cookie-accept-all').click(timeout=2000)
            page.wait_for_timeout(500)
            print("Accepted cookies")
        except Exception as e2:
            print(f"Could not click accept either: {e2}")

    # Now try hamburger again
    try:
        hamburger = page.locator('#mobile-menu-btn')
        hamburger.click(timeout=2000)
        page.wait_for_timeout(500)
        print("Hamburger clicked successfully (after cookie dismiss)")

        menu_visible = page.evaluate("""
            !document.getElementById('mobile-menu')?.classList.contains('hidden')
        """)
        print(f"Mobile menu appeared: {menu_visible}")
    except Exception as e:
        print(f"Hamburger click failed after dismiss: {e}")

    context.close()

    # ====== posicionamiento-web-asturias overflow check ======
    print("\n" + "=" * 60)
    print("posicionamiento-web-asturias OVERFLOW ROOT CAUSE")
    print("=" * 60)

    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(BASE_URL + "/posicionamiento-web-asturias/", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    overflow_cause = page.evaluate("""
        () => {
            const r = {};
            r.scrollWidth = document.documentElement.scrollWidth;
            r.viewportWidth = window.innerWidth;
            r.overflowX = document.documentElement.scrollWidth - window.innerWidth;

            // Find which elements are wider than viewport
            r.wideElements = [];
            document.querySelectorAll('*').forEach(el => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                if (rect.width > window.innerWidth + 5 &&
                    style.display !== 'none' &&
                    style.visibility !== 'hidden' &&
                    el.offsetParent !== null &&
                    !['SCRIPT', 'STYLE', 'LINK', 'META', 'HEAD'].includes(el.tagName)) {
                    r.wideElements.push({
                        tag: el.tagName,
                        width: Math.round(rect.width),
                        left: Math.round(rect.left),
                        text: el.textContent.trim().substring(0, 60),
                        class: el.className.substring(0, 80),
                        overflow: style.overflow,
                        overflowX: style.overflowX,
                    });
                }
            });

            // Only show top 15 widest
            r.wideElements.sort((a, b) => b.width - a.width);
            r.wideElements = r.wideElements.slice(0, 15);

            // Check body/html overflow
            r.htmlOverflowX = window.getComputedStyle(document.documentElement).overflowX;
            r.bodyOverflowX = window.getComputedStyle(document.body).overflowX;

            // Check images that might overflow
            r.wideImages = [];
            document.querySelectorAll('img, video, iframe, pre, table').forEach(el => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                if (rect.width > window.innerWidth && el.offsetParent !== null) {
                    r.wideImages.push({
                        tag: el.tagName,
                        width: Math.round(rect.width),
                        maxWidth: style.maxWidth,
                        src: el.src?.substring(0, 80) || '',
                        class: el.className.substring(0, 60),
                    });
                }
            });

            return r;
        }
    """)

    print(f"Document scrollWidth: {overflow_cause.get('scrollWidth')}px")
    print(f"Viewport width: {overflow_cause.get('viewportWidth')}px")
    print(f"Overflow: {overflow_cause.get('overflowX')}px")
    print(f"HTML overflow-x: {overflow_cause.get('htmlOverflowX')}")
    print(f"Body overflow-x: {overflow_cause.get('bodyOverflowX')}")
    print(f"\nWide elements (top 15):")
    for el in overflow_cause.get('wideElements', []):
        print(f"  <{el['tag']}> cls='{el['class']}' width={el['width']}px left={el['left']}px text='{el['text']}'")
    print(f"\nWide images: {overflow_cause.get('wideImages', [])}")

    context.close()

    browser.close()
    print("\n=== Final checks complete ===")
