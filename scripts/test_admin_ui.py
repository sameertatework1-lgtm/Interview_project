from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    page.goto("https://automationintesting.online/admin", wait_until="domcontentloaded")
    page.wait_for_selector("#username")
    page.fill("#username", "admin")
    page.fill("#password", "password")
    page.click("#doLogin")
    page.wait_for_timeout(3000)
    print("Logged In URL:", page.url)
    print("Cookies:", ctx.cookies())
    inputs = page.locator("input").all()
    print("Inputs after login:", len(inputs))
    for i in inputs:
        print(
            "  Input:",
            i.get_attribute("id"),
            i.get_attribute("placeholder"),
            i.get_attribute("name"),
        )
    buttons = page.locator("button").all()
    print("Buttons after login:", len(buttons))
    for b in buttons:
        print("  Button:", b.inner_text(), b.get_attribute("id"))
    links = page.locator("a").all()
    print("Links after login:", len(links))
    for link in links:
        print("  Link:", link.inner_text(), link.get_attribute("href"))
    print("Page text snippet:", page.locator("body").inner_text()[:600])
    browser.close()
