from playwright.sync_api import Page, expect


def test_tc001_login_with_valid_credentials(page: Page):
    page.goto("http://127.0.0.1:8000/login.html")

    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(
        page.get_by_role("heading", name="Dashboard")
    ).to_be_visible()

