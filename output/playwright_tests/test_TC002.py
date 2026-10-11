from playwright.sync_api import Page, expect


def test_tc002_login_with_invalid_email(page: Page):
    page.goto("http://127.0.0.1:8000/login.html")

    page.get_by_label("Email").fill("wrong@example.com")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Invalid email")

