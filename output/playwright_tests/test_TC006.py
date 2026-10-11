from playwright.sync_api import Page, expect


def test_tc006_login_with_empty_password(page: Page):
    page.goto("http://127.0.0.1:8000/login.html")

    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Password is required")

