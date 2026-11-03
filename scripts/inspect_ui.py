from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    created_reqs = []

    def on_req(req):
        if "/api/" in req.url:
            created_reqs.append(
                {
                    "url": req.url,
                    "method": req.method,
                    "headers": req.headers,
                }
            )

    page.on("request", on_req)

    print("Going to admin...")
    page.goto("https://automationintesting.online/#/admin")
    page.wait_for_selector('#username, input[placeholder="Username"]')
    page.fill('#username, input[placeholder="Username"]', "admin")
    page.fill('#password, input[placeholder="Password"]', "password")
    page.click('#doLogin, button:has-text("Login")')
    page.wait_for_timeout(3000)
    print("Cookies in context:", context.cookies())

    for r in created_reqs:
        print(f"{r['method']} {r['url']}")
        print(
            "  Headers:",
            {k: v for k, v in r["headers"].items() if k.lower() in ("cookie", "authorization")},
        )

    # Now try creating a room via UI and see what is sent!
    if page.locator("#roomName").count() > 0:
        print("Creating room via UI...")
        page.fill("#roomName", "AUTO_TEST_UI_99")
        page.select_option("#type", "Double")
        page.select_option("#accessible", "true")
        page.fill("#roomPrice", "150")
        page.click("#createRoom")
        page.wait_for_timeout(2000)

    for r in created_reqs[-3:]:
        print(f"AFTER ACTION: {r['method']} {r['url']}")
        print(
            "  Headers:",
            {k: v for k, v in r["headers"].items() if k.lower() in ("cookie", "authorization")},
        )

    browser.close()
