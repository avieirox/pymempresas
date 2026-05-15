"""Targeted checks: mobile nav, contact form, breakpoints, tap targets, color contrast."""
import sys
sys.path.insert(0, r'C:\Users\aviei\AppData\Roaming\Python\Python312\site-packages')

from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://pymempresas.com"

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ====== DEEP DIVE: Mobile navigation ======
    print("=" * 60)
    print("MOBILE NAVIGATION DEEP DIVE (375x812)")
    print("=" * 60)

    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    nav_info = page.evaluate("""
        () => {
            const r = {};
            // Find ALL interactive elements at top of page
            const header = document.querySelector('header') || document.querySelector('[class*="nav" i]') || document.querySelector('nav');
            if (header) {
                r.headerHTML = header.innerHTML.substring(0, 2000);
                r.headerClasses = header.className;
                r.headerTag = header.tagName;
            }

            // Find all buttons
            const buttons = document.querySelectorAll('button');
            r.buttons = [];
            buttons.forEach(b => {
                const rect = b.getBoundingClientRect();
                r.buttons.push({
                    text: b.textContent.trim().substring(0, 50),
                    class: b.className,
                    id: b.id,
                    type: b.type || 'N/A',
                    ariaLabel: b.getAttribute('aria-label') || '',
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    top: Math.round(rect.top),
                    visible: rect.width > 0 && rect.height > 0 && b.offsetParent !== null,
                });
            });

            // Check if there's a mobile menu toggle that we missed
            r.allPotentialToggles = [];
            document.querySelectorAll('[class*="menu" i], [class*="toggle" i], [class*="hamburger" i], [class*="navbar" i], [class*="mobile" i], [id*="menu" i], [id*="toggle" i]').forEach(el => {
                r.allPotentialToggles.push({
                    tag: el.tagName,
                    class: el.className,
                    id: el.id,
                    text: el.textContent.trim().substring(0, 40),
                });
            });

            // Check visible nav links in viewport
            r.visibleTopLinks = [];
            document.querySelectorAll('a').forEach(a => {
                const rect = a.getBoundingClientRect();
                const style = window.getComputedStyle(a);
                if (rect.top < 100 && rect.width > 0 && style.display !== 'none' && style.visibility !== 'hidden' && a.offsetParent !== null) {
                    r.visibleTopLinks.push({
                        text: a.textContent.trim().substring(0, 40),
                        href: a.getAttribute('href')?.substring(0, 60) || '',
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        top: Math.round(rect.top),
                    });
                }
            });

            // Check the hamburger icon (maybe it uses Tabler Icons class)
            r.tablerIcons = [];
            document.querySelectorAll('i[class*="ti-"], span[class*="ti-"]').forEach(icon => {
                const rect = icon.getBoundingClientRect();
                if (rect.top < 100 && rect.width > 0) {
                    r.tablerIcons.push({
                        class: icon.className,
                        top: Math.round(rect.top),
                        width: Math.round(rect.width),
                        parent: icon.parentElement?.tagName,
                        parentText: icon.parentElement?.textContent?.trim()?.substring(0,30) || '',
                    });
                }
            });

            // Check the SVG icon patterns
            r.svgButtons = [];
            document.querySelectorAll('header svg, nav svg, [class*="nav"] svg').forEach(svg => {
                const rect = svg.getBoundingClientRect();
                if (rect.top < 100) {
                    r.svgButtons.push({
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        top: Math.round(rect.top),
                        parent: svg.parentElement?.tagName,
                        parentClass: svg.parentElement?.className?.substring(0, 80),
                    });
                }
            });

            return r;
        }
    """)

    print("Header HTML (first 2000 chars):")
    print(nav_info.get('headerHTML', 'N/A'))
    print("\n--- Buttons in header ---")
    for b in nav_info.get('buttons', []):
        print(f"  <{b['type']}> '{b['text']}' cls='{b['class']}' id='{b['id']}' label='{b['ariaLabel']}' size={b['width']}x{b['height']} visible={b['visible']}")

    print("\n--- Potential mobile menu toggles ---")
    for t in nav_info.get('allPotentialToggles', []):
        print(f"  <{t['tag']}> cls='{t['class']}' id='{t['id']}' text='{t['text']}'")

    print("\n--- Visible top links (y<100) ---")
    for a in nav_info.get('visibleTopLinks', []):
        print(f"  '{a['text']}' href='{a['href']}' {a['width']}x{a['height']}px at y={a['top']}")

    print("\n--- Tabler Icons in header area ---")
    for icon in nav_info.get('tablerIcons', []):
        print(f"  cls='{icon['class']}' y={icon['top']} parent=<{icon['parent']}> text='{icon['parentText']}'")

    print("\n--- SVG buttons in nav ---")
    for svg in nav_info.get('svgButtons', []):
        print(f"  {svg['width']}x{svg['height']}px at y={svg['top']} parent=<{svg['parent']}> cls='{svg['parentClass']}'")

    context.close()

    # ====== CHECK: contacto page form ======
    print("\n" + "=" * 60)
    print("CONTACTO PAGE FORM CHECK")
    print("=" * 60)

    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(BASE_URL + "/contacto/", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    form_check = page.evaluate("""
        () => {
            const r = {};
            const forms = document.querySelectorAll('form');
            r.formCount = forms.length;
            r.forms = [];
            forms.forEach((f, i) => {
                const inputs = f.querySelectorAll('input, textarea, select, button');
                const rect = f.getBoundingClientRect();
                r.forms.push({
                    index: i,
                    action: f.action || '',
                    method: f.method || '',
                    inputs: inputs.length,
                    top: Math.round(rect.top),
                    visibleAboveFold: rect.top < window.innerHeight,
                    height: Math.round(rect.height),
                });
                // Check each input
                r.forms[i].fields = [];
                inputs.forEach(inp => {
                    const ir = inp.getBoundingClientRect();
                    r.forms[i].fields.push({
                        tag: inp.tagName,
                        type: inp.type || '',
                        name: inp.name || inp.id || '',
                        placeholder: inp.placeholder || '',
                        width: Math.round(ir.width),
                        height: Math.round(ir.height),
                        top: Math.round(ir.top),
                    });
                });
            });

            // Check if contact info is visible above fold
            r.contactInfo = [];
            document.querySelectorAll('[class*="contact" i] a[href^="tel"], [class*="contact" i] a[href^="mailto"], a[href^="tel:"], a[href^="mailto:"]').forEach(a => {
                const rect = a.getBoundingClientRect();
                r.contactInfo.push({
                    href: a.getAttribute('href')?.substring(0, 60),
                    text: a.textContent.trim(),
                    top: Math.round(rect.top),
                    visibleInViewport: rect.top < window.innerHeight,
                });
            });

            r.address = [];
            document.querySelectorAll('p, span, div').forEach(el => {
                const text = el.textContent.trim();
                if ((text.includes('Gij') || text.includes('Asturias') || text.includes('Coworking')) && text.length > 10 && text.length < 150) {
                    const rect = el.getBoundingClientRect();
                    r.address.push({
                        text: text.substring(0, 100),
                        top: Math.round(rect.top),
                        visibleAboveFold: rect.top < window.innerHeight,
                    });
                }
            });

            return r;
        }
    """)

    print(f"Forms found: {form_check.get('formCount')}")
    for f in form_check.get('forms', []):
        v = "ABOVE FOLD" if f['visibleAboveFold'] else "below fold"
        print(f"  Form #{f['index']}: {f['inputs']} inputs, {v}, top y={f['top']}, height={f['height']}px")
        for field in f['fields']:
            print(f"    <{field['tag']}> type={field['type']} name={field['name']} placeholder='{field['placeholder']}' {field['width']}x{field['height']}px")

    print("\n--- Contact Info ---")
    for c in form_check.get('contactInfo', []):
        print(f"  {c['href']} - \"{c['text']}\" y={c['top']} (fold: {c['visibleInViewport']})")

    print("\n--- Address ---")
    for a in form_check.get('address', []):
        print(f"  \"{a['text']}\" y={a['top']} (fold: {a['visibleAboveFold']})")

    context.close()

    # ====== CHECK: 768px breakpoint behavior ======
    print("\n" + "=" * 60)
    print("TABLET BREAKPOINT (768x1024)")
    print("=" * 60)

    context = browser.new_context(viewport={"width": 768, "height": 1024})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    tablet = page.evaluate("""
        () => {
            const r = {};
            // How are nav links displayed at tablet?
            r.navDisplay = {};
            document.querySelectorAll('header a, nav a').forEach(a => {
                const style = window.getComputedStyle(a);
                const rect = a.getBoundingClientRect();
                const key = a.textContent.trim() || '(logo)';
                if (rect.top < 100 && rect.width > 0) {
                    r.navDisplay[key] = {
                        display: style.display,
                        width: Math.round(rect.width),
                        top: Math.round(rect.top),
                    };
                }
            });

            // Check any hidden/overflow-x issues
            r.overflow = document.documentElement.scrollWidth - window.innerWidth;

            // Check if page has horizontal scroll at 768px
            r.bodyOverflowX = window.getComputedStyle(document.body).overflowX;

            return r;
        }
    """)

    print(f"Overflow: {tablet.get('overflow')}px, body overflow-x: {tablet.get('bodyOverflowX')}")
    print("Nav links visible at top:")
    for k, v in tablet.get('navDisplay', {}).items():
        print(f"  '{k}': display={v['display']} width={v['width']}px y={v['top']}")

    context.close()

    # ====== CHECK: Mobile hamburger menu functionality ======
    print("\n" + "=" * 60)
    print("HAMBURGER MENU FUNCTIONALITY TEST")
    print("=" * 60)

    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    # Dismiss cookie banner first
    try:
        reject_btn = page.locator('button:has-text("Rechazar todas")')
        if reject_btn.is_visible(timeout=2000):
            reject_btn.click()
            page.wait_for_timeout(500)
            print("Cookie banner dismissed")
    except:
        print("Could not dismiss cookie banner")

    # Now look for and try clicking hamburger
    click_result = page.evaluate("""
        () => {
            const r = {};
            // Try to find ANY button that expands the menu
            const allBtn = document.querySelectorAll('button');
            for (const btn of allBtn) {
                const rect = btn.getBoundingClientRect();
                if (rect.top < 60 && rect.width > 20 && rect.height > 20 && btn.offsetParent !== null) {
                    // This might be the hamburger - try clicking it
                    r.foundToggle = {
                        text: btn.textContent.trim().substring(0, 30),
                        class: btn.className,
                        size: Math.round(rect.width) + 'x' + Math.round(rect.height),
                    };
                    break;
                }
            }
            return r;
        }
    """)

    print(f"Potential toggle found: {click_result.get('foundToggle', 'none')}")

    # After dismissing cookie, check how many nav links are now visible
    if click_result.get('foundToggle'):
        toggle_btn = page.locator('button').first
        # Try clicking the first button in header area
        page.evaluate("""
            () => {
                const btns = document.querySelectorAll('button');
                for (const btn of btns) {
                    const rect = btn.getBoundingClientRect();
                    if (rect.top < 60 && rect.width > 20 && rect.height > 20 && btn.offsetParent !== null) {
                        btn.click();
                        return btn.className;
                    }
                }
                return 'none found';
            }
        """)
        page.wait_for_timeout(500)

        # Check what's visible now
        after_click = page.evaluate("""
            () => {
                const links = document.querySelectorAll('header a, nav a');
                let visible = 0, total = 0;
                const details = [];
                links.forEach(a => {
                    total++;
                    const rect = a.getBoundingClientRect();
                    const style = window.getComputedStyle(a);
                    if (a.offsetParent !== null && style.display !== 'none' && style.visibility !== 'hidden') {
                        visible++;
                        if (rect.top < 800) {
                            details.push({
                                text: a.textContent.trim().substring(0, 30),
                                href: a.getAttribute('href')?.substring(0, 50),
                                top: Math.round(rect.top),
                            });
                        }
                    }
                });
                return {visible, total, details};
            }
        """)
        print(f"After click: {after_click.get('visible')}/{after_click.get('total')} links visible")
        for d in after_click.get('details', [])[:15]:
            print(f"  '{d['text']}' -> {d['href']} at y={d['top']}")

    context.close()

    # ====== WCAG Color Contrast Check ======
    print("\n" + "=" * 60)
    print("COLOR CONTRAST CHECK")
    print("=" * 60)

    # Orange #F5A623 on Black #0A0A0A
    # WCAG AA requires 4.5:1 for normal text, 3:1 for large text
    # Relative luminance formula
    def rel_lum(r, g, b):
        def channel(c):
            c = c / 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    # Orange #F5A623 = rgb(245, 166, 35)
    orange_lum = rel_lum(245, 166, 35)
    # Black #0A0A0A = rgb(10, 10, 10)
    black_lum = rel_lum(10, 10, 10)
    # White #FFFFFF for text on black
    white_lum = rel_lum(255, 255, 255)

    def contrast_ratio(l1, l2):
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    orange_on_black = contrast_ratio(orange_lum, black_lum)
    white_on_black = contrast_ratio(white_lum, black_lum)

    print(f"Orange #F5A623 on Black #0A0A0A: {orange_on_black:.2f}:1 (WCAG AA large text needs 3:1, normal text needs 4.5:1)")
    print(f"White text on Black bg: {white_on_black:.2f}:1")

    # Check what colors the actual buttons use
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)

    colors = page.evaluate("""
        () => {
            const r = {};
            // Main CTA button
            const cta = document.querySelector('a:has-text("Solicitar")');
            if (cta) {
                const style = window.getComputedStyle(cta);
                r.ctaStyle = {
                    bg: style.backgroundColor,
                    color: style.color,
                    border: style.border,
                    fontSize: style.fontSize,
                    fontWeight: style.fontWeight,
                    padding: style.padding,
                };
            }

            // Body text
            r.bodyStyle = {
                color: window.getComputedStyle(document.body).color,
                bg: window.getComputedStyle(document.body).backgroundColor,
                fontSize: window.getComputedStyle(document.body).fontSize,
            };

            // H1
            const h1 = document.querySelector('h1');
            if (h1) {
                r.h1Style = {
                    color: window.getComputedStyle(h1).color,
                    fontSize: window.getComputedStyle(h1).fontSize,
                    fontWeight: window.getComputedStyle(h1).fontWeight,
                };
            }

            return r;
        }
    """)

    print(f"\nActual styles from homepage:")
    print(f"  Body: color={colors.get('bodyStyle',{}).get('color')} bg={colors.get('bodyStyle',{}).get('bg')} size={colors.get('bodyStyle',{}).get('fontSize')}")
    print(f"  H1: color={colors.get('h1Style',{}).get('color')} size={colors.get('h1Style',{}).get('fontSize')} weight={colors.get('h1Style',{}).get('fontWeight')}")
    print(f"  CTA button: bg={colors.get('ctaStyle',{}).get('bg')} color={colors.get('ctaStyle',{}).get('color')} size={colors.get('ctaStyle',{}).get('fontSize')} weight={colors.get('ctaStyle',{}).get('fontWeight')}")
    context.close()

    browser.close()
    print("\n=== Targeted checks complete ===")
