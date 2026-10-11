from playwright.sync_api import Page, expect


def test_tc007_login_with_invalid_email_format(page: Page):
    page.goto("http://127.0.0.1:8000/login.html")

    page.get_by_label("Email").fill("manu@")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Invalid email format")

