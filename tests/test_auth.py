import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL, USERS, do_login


class TestLogin:

    def test_standard_login(self, page: Page):
        do_login(page, "standard")
        expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    def test_products_heading_visible(self, page: Page):
        do_login(page, "standard")
        expect(page.locator(".title")).to_have_text("Products")

    def test_locked_user_gets_error(self, page: Page):
        do_login(page, "locked")
        expect(page.locator("[data-test='error']")).to_contain_text("locked out")

    def test_problem_user_can_login(self, page: Page):
        """problem_user logs in fine but has broken images — we just check login works"""
        do_login(page, "problem")
        expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    #form validation

    def test_empty_username_shows_error(self, page: Page):
        page.goto(BASE_URL)
        page.fill("[data-test='password']", "secret_sauce")
        page.click("[data-test='login-button']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_empty_password_shows_error(self, page: Page):
        page.goto(BASE_URL)
        page.fill("[data-test='username']", "standard_user")
        page.click("[data-test='login-button']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_both_empty(self, page: Page):
        page.goto(BASE_URL)
        page.click("[data-test='login-button']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_bad_password(self, page: Page):
        page.goto(BASE_URL)
        page.fill("[data-test='username']", "standard_user")
        page.fill("[data-test='password']", "nope")
        page.click("[data-test='login-button']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_dismiss_error(self, page: Page):
        page.goto(BASE_URL)
        page.click("[data-test='login-button']")
        page.click(".error-button")
        expect(page.locator("[data-test='error']")).not_to_be_visible()

    #UI element checks

    def test_login_button_present(self, page: Page):
        page.goto(BASE_URL)
        expect(page.locator("[data-test='login-button']")).to_be_visible()

    def test_username_placeholder(self, page: Page):
        page.goto(BASE_URL)
        expect(page.locator("[data-test='username']")).to_have_attribute(
            "placeholder", "Username"
        )

    def test_password_placeholder(self, page: Page):
        page.goto(BASE_URL)
        expect(page.locator("[data-test='password']")).to_have_attribute(
            "placeholder", "Password"
        )
