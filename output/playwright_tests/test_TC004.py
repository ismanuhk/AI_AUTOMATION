from playwright.sync_api import Page, expect


def test_tc004_login_with_both_fields_empty(page: Page):
    page.goto("http://127.0.0.1:8000/login.html")

    page.get_by_label("Email").fill("")
    page.get_by_label("Password").fill("")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text(
        "Email and password are required"
    )

