"""Deep visual analysis of pymempresas.com"""
import sys
sys.path.insert(0, r'C:\Users\aviei\AppData\Roaming\Python\Python312\site-packages')

from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://pymempresas.com"
OUTPUT_DIR = r"C:\Users\aviei\Documents\Pymempresas\pymempresas-web\screenshots"

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Test at all 4 viewports
    for device_name, width, height in [
        ("desktop", 1920, 1080),
        ("laptop", 1366, 768),
        ("tablet", 768, 1024),
        ("mobile", 375, 812),
    ]:
        print(f"\n{'='*60}")
        print(f"VIEWPORT: {device_name} ({width}x{height})")
        print(f"{'='*60}")

        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
        )
        page = context.new_page()

        try:
            page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            results = page.evaluate("""
                () => {
                    const r = {};
                    const vp = {w: window.innerWidth, h: window.innerHeight};

                    // 1. Check navigation on mobile
                    r.hamburger = (() => {
                        const btns = document.querySelectorAll('button, a[role="button"]');
                        for (const b of btns) {
                            const html = b.innerHTML.toLowerCase();
                            const cls = b.className.toLowerCase();
                            const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                            if (html.includes('menu') || html.includes('hamburger') || html.includes('ti-menu') ||
                                html.includes('ti-align') || html.includes('bars') || cls.includes('hamburger') ||
                                cls.includes('menu-toggle') || cls.includes('navbar-toggle') || aria.includes('menu'))
                                return {found: true, tag: b.tagName, class: b.className, html: b.innerHTML.substring(0,100)};
                        }
                        return {found: false};
                    })();

                    // Check if nav links are visible
                    r.navLinksVisible = (() => {
                        const links = document.querySelectorAll('nav a, header a');
                        let visible = 0, hidden = 0;
                        links.forEach(a => {
                            const style = window.getComputedStyle(a);
                            if (style.display !== 'none' && style.visibility !== 'hidden' && a.offsetParent !== null)
                                visible++;
                            else
                                hidden++;
                        });
                        return {visible, hidden};
                    })();

                    // 2. CTA buttons above fold - check visibility and size
                    r.ctaButtons = [];
                    document.querySelectorAll('a, button').forEach(el => {
                        const text = el.textContent.trim();
                        if (!text) return;
                        const rect = el.getBoundingClientRect();
                        const isAboveFold = rect.top < vp.h;
                        const isCTA = text.toLowerCase().includes('consult') || text.toLowerCase().includes('servicio') ||
                                     text.toLowerCase().includes('presupuesto') || text.toLowerCase().includes('contact') ||
                                     text.toLowerCase().includes('mensaje') || text.toLowerCase().includes('aceptar') ||
                                     text.toLowerCase().includes('rechazar') || text.toLowerCase().includes('guardar');

                        if ((isCTA || (isAboveFold && (el.tagName === 'BUTTON' || (el.tagName === 'A' && el.href))))) {
                            const style = window.getComputedStyle(el);
                            r.ctaButtons.push({
                                tag: el.tagName,
                                text: text.substring(0, 60),
                                top: Math.round(rect.top),
                                bottom: Math.round(rect.bottom),
                                width: Math.round(rect.width),
                                height: Math.round(rect.height),
                                aboveFold: isAboveFold,
                                bg: style.backgroundColor,
                                color: style.color,
                                fontSize: style.fontSize,
                                display: style.display,
                                visibility: style.visibility,
                                zIndex: style.zIndex,
                                position: style.position,
                                pointerEvents: style.pointerEvents,
                            });
                        }
                    });

                    // 3. Check font size of body text
                    r.bodyFontSize = window.getComputedStyle(document.body).fontSize;

                    // 4. Check if cookie banner blocks content
                    r.cookieBanner = (() => {
                        const cookie = document.querySelector('[class*="cookie" i], [class*="Cookie" i], [id*="cookie" i], [id*="Cookie" i], [class*="consent" i]');
                        if (!cookie) return {present: false};
                        const rect = cookie.getBoundingClientRect();
                        const style = window.getComputedStyle(cookie);
                        return {
                            present: true,
                            top: Math.round(rect.top),
                            bottom: Math.round(rect.bottom),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            zIndex: style.zIndex,
                            position: style.position,
                            bg: style.backgroundColor,
                            occupiesFullScreen: rect.top <= 0 && rect.bottom >= vp.h,
                        };
                    })();

                    // 5. Check for horizontal scroll
                    r.horizontalScroll = document.documentElement.scrollWidth - window.innerWidth;

                    // 6. Check hero image
                    r.heroSection = (() => {
                        const hero = document.querySelector('[class*="hero" i], section:first-of-type, main > section:first-child');
                        if (!hero) return {found: false};
                        const rect = hero.getBoundingClientRect();
                        const bg = window.getComputedStyle(hero).backgroundImage;
                        return {
                            found: true,
                            top: Math.round(rect.top),
                            height: Math.round(rect.height),
                            hasBgImage: bg !== 'none',
                            bgImage: bg.substring(0,100),
                        };
                    })();

                    // 7. Check logo
                    r.logo = (() => {
                        const imgs = document.querySelectorAll('header img, nav img');
                        for (const img of imgs) {
                            if (img.alt !== undefined) {
                                return {src: img.src, alt: img.alt, width: img.width, height: img.height};
                            }
                        }
                        return null;
                    })();

                    // 8. Font loads (check Inter)
                    r.interFontLoaded = document.fonts.check('16px Inter');

                    // 9. Tap target audit (mobile)
                    r.tapTargetIssues = [];
                    if (vp.w <= 768) {
                        const clickables = document.querySelectorAll('a, button, input, select, textarea');
                        clickables.forEach(el => {
                            const rect = el.getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0 && rect.top < vp.h) {
                                const text = el.textContent.trim().substring(0, 40);
                                if (rect.width < 48 || rect.height < 48) {
                                    r.tapTargetIssues.push({
                                        tag: el.tagName,
                                        text: text,
                                        width: Math.round(rect.width),
                                        height: Math.round(rect.height),
                                        top: Math.round(rect.top),
                                    });
                                }
                            }
                        });
                    }

                    // 10. Color contrast (orange #F5A623 on black #0A0A0A) - basic check
                    r.themeColors = {
                        bodyBg: window.getComputedStyle(document.body).backgroundColor,
                        bodyColor: window.getComputedStyle(document.body).color,
                    };

                    // 11. Form visibility on contacto page
                    r.formStatus = (() => {
                        const forms = document.querySelectorAll('form');
                        return forms.length > 0 ? forms.length + ' form(s) found' : 'no forms';
                    })();

                    // 12. Collect all H tags hierarchy
                    r.headings = [];
                    document.querySelectorAll('h1, h2, h3, h4').forEach(h => {
                        const rect = h.getBoundingClientRect();
                        r.headings.push({
                            tag: h.tagName,
                            text: h.textContent.trim().substring(0, 60),
                            top: Math.round(rect.top),
                            visible: rect.top < vp.h && rect.bottom > 0,
                        });
                    });

                    return r;
                }
            """)

            print(f"Body font size: {results.get('bodyFontSize')}")
            print(f"Inter font loaded: {results.get('interFontLoaded')}")
            print(f"Theme colors: bodyBg={results.get('themeColors',{}).get('bodyBg')}, bodyColor={results.get('themeColors',{}).get('bodyColor')}")
            print(f"Horizontal scroll overflow: {results.get('horizontalScroll')}px")
            print(f"Hero section: {json.dumps(results.get('heroSection'), indent=2)}")
            print(f"Logo: {json.dumps(results.get('logo'), indent=2)}")
            print(f"Navigation: menu_hamburger={results.get('hamburger')}, links_visible={results.get('navLinksVisible')}")
            print(f"Cookie banner: {json.dumps(results.get('cookieBanner'), indent=2)}")
            print(f"Form status: {results.get('formStatus')}")

            print(f"\n--- CTA Buttons ({len(results.get('ctaButtons',[]))} found) ---")
            for cta in results.get('ctaButtons', []):
                abv = "ABOVE-FOLD" if cta['aboveFold'] else "below-fold"
                print(f"  [{abv}] <{cta['tag']}> {cta['text']} | size={cta['width']}x{cta['height']}px | font={cta['fontSize']} | bg={cta['bg']} | z={cta['zIndex']} | visible={cta['visibility']}")

            if results.get('tapTargetIssues'):
                print(f"\n=== TAP TARGET ISSUES ({len(results['tapTargetIssues'])} found) ===")
                for t in results['tapTargetIssues'][:10]:
                    print(f"  <{t['tag']}> '{t['text']}' {t['width']}x{t['height']}px at y={t['top']}")

            print(f"\n--- Headings ---")
            for h in results.get('headings', []):
                v = "VISIBLE" if h['visible'] else "below-fold"
                print(f"  [{v}] <{h['tag']}> y={h['top']}: {h['text']}")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            context.close()

    # Now test service pages on mobile specifically
    print(f"\n{'='*60}")
    print(f"SERVICE PAGES - MOBILE ANALYSIS")
    print(f"{'='*60}")

    service_pages = [
        "/seo-local-gijon/",
        "/diseno-web-gijon/",
        "/posicionamiento-web-asturias/",
    ]

    for path in service_pages:
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            device_scale_factor=2,  # Retina for realistic mobile
        )
        page = context.new_page()
        try:
            page.goto(BASE_URL + path, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            r = page.evaluate("""
                () => {
                    const vp = {w: window.innerWidth, h: window.innerHeight};
                    const data = {};

                    data.h1 = document.querySelector('h1')?.textContent?.trim() || '';
                    data.h1Visible = (() => {
                        const h1 = document.querySelector('h1');
                        if (!h1) return false;
                        const r = h1.getBoundingClientRect();
                        return r.top < vp.h && r.bottom > 0;
                    })();

                    // Check all CTA buttons
                    data.ctas = [];
                    document.querySelectorAll('a, button').forEach(el => {
                        const text = el.textContent.trim().toLowerCase();
                        if (text.includes('consult') || text.includes('presupuesto') || text.includes('servicio') || text.includes('precio') || text.includes('portfolio')) {
                            const rect = el.getBoundingClientRect();
                            const style = window.getComputedStyle(el);
                            data.ctas.push({
                                text: el.textContent.trim().substring(0,50),
                                top: Math.round(rect.top),
                                bot: Math.round(rect.bottom),
                                height: rect.height,
                                visible: rect.top < vp.h,
                                bg: style.backgroundColor,
                                color: style.color,
                                zIndex: style.zIndex,
                                position: style.position,
                            });
                        }
                    });

                    // Check hero section
                    data.heroText = [];
                    document.querySelectorAll('[class*="hero"] h1, [class*="hero"] p, [class*="hero"] span, section:first-of-type p, section:first-of-type span').forEach(el => {
                        if (el.textContent.trim()) {
                            const rect = el.getBoundingClientRect();
                            data.heroText.push({
                                text: el.textContent.trim().substring(0,80),
                                top: Math.round(rect.top),
                                visible: rect.top < vp.h && rect.bottom > 0,
                                fontSize: window.getComputedStyle(el).fontSize,
                            });
                        }
                    });

                    // Check for any visible elements overlapping
                    data.cookieOverlapsCTA = (() => {
                        const cookie = document.querySelector('[class*="cookie" i], [class*="Cookie" i]');
                        if (!cookie) return false;
                        const cookieRect = cookie.getBoundingClientRect();
                        const ctas = document.querySelectorAll('a, button');
                        for (const cta of ctas) {
                            const text = cta.textContent.trim().toLowerCase();
                            if (text.includes('consult') || text.includes('presupuesto') || text.includes('servicio')) {
                                const rect = cta.getBoundingClientRect();
                                if (rect.top < cookieRect.bottom && rect.bottom > cookieRect.top) {
                                    return true;
                                }
                            }
                        }
                        return false;
                    })();

                    data.scrollWidth = document.documentElement.scrollWidth;
                    data.viewportWidth = vp.w;

                    return data;
                }
            """)

            print(f"\n--- {path} ---")
            print(f"  H1: {r.get('h1')} (visible: {r.get('h1Visible')})")
            print(f"  Scroll: {r.get('scrollWidth')}px width vs {r.get('viewportWidth')}px viewport")
            print(f"  Cookie overlaps CTA: {r.get('cookieOverlapsCTA')}")
            for cta in r.get('ctas', []):
                v = "VISIBLE" if cta['visible'] else "BELOW-FOLD"
                print(f"  CTA [{v}]: '{cta['text']}' y={cta['top']}-{cta['bot']} size={cta['height']}px bg={cta['bg']}")

        except Exception as e:
            print(f"  ERROR on {path}: {e}")
        finally:
            context.close()

    browser.close()
    print("\n=== Analysis complete ===")
