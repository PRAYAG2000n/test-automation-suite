import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL

# all the add-to-cart button data-test ids
BACKPACK_BTN   = "add-to-cart-sauce-labs-backpack"
BIKELIGHT_BTN  = "add-to-cart-sauce-labs-bike-light"
BOLT_BTN       = "add-to-cart-sauce-labs-bolt-t-shirt"
FLEECE_BTN     = "add-to-cart-sauce-labs-fleece-jacket"
ONESIE_BTN     = "add-to-cart-sauce-labs-onesie"
ALLTHINGS_BTN  = "add-to-cart-test.allthethings()-t-shirt-(red)"


def add_item(page: Page, btn_id: str):
    page.click(f"[data-test='{btn_id}']")


def go_to_cart(page: Page):
    page.click("[data-test='shopping-cart-link']")


class TestAddRemove:

    def test_cart_starts_empty(self, logged_in_page: Page):
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator(".cart_item")).to_have_count(0)

    def test_add_one_item(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator(".cart_item")).to_have_count(1)

    def test_add_two_items(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        add_item(logged_in_page, BIKELIGHT_BTN)
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator(".cart_item")).to_have_count(2)

    def test_remove_from_cart_page(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        go_to_cart(logged_in_page)
        logged_in_page.click("[data-test='remove-sauce-labs-backpack']")
        expect(logged_in_page.locator(".cart_item")).to_have_count(0)

    def test_remove_from_inventory_page(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        logged_in_page.click("[data-test='remove-sauce-labs-backpack']")
        expect(
            logged_in_page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
        ).to_be_visible()

    def test_add_all_six(self, logged_in_page: Page):
        for btn in [BACKPACK_BTN, BIKELIGHT_BTN, BOLT_BTN, FLEECE_BTN, ONESIE_BTN, ALLTHINGS_BTN]:
            add_item(logged_in_page, btn)
        badge = logged_in_page.locator("[data-test='shopping-cart-badge']")
        expect(badge).to_have_text("6")


class TestCartBadge:

    def test_badge_shows_1(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        expect(
            logged_in_page.locator("[data-test='shopping-cart-badge']")
        ).to_have_text("1")

    def test_badge_increments(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        add_item(logged_in_page, BIKELIGHT_BTN)
        expect(
            logged_in_page.locator("[data-test='shopping-cart-badge']")
        ).to_have_text("2")

    def test_badge_disappears_when_empty(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        logged_in_page.click("[data-test='remove-sauce-labs-backpack']")
        expect(
            logged_in_page.locator("[data-test='shopping-cart-badge']")
        ).not_to_be_visible()


class TestCartPage:

    def test_item_name_shown(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator(".inventory_item_name")).to_have_text(
            "Sauce Labs Backpack"
        )

    def test_item_price_shown(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator(".inventory_item_price")).to_have_text("$29.99")

    def test_quantity_is_one(self, logged_in_page: Page):
        add_item(logged_in_page, BACKPACK_BTN)
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator(".cart_quantity")).to_have_text("1")

    def test_continue_shopping(self, logged_in_page: Page):
        go_to_cart(logged_in_page)
        logged_in_page.click("[data-test='continue-shopping']")
        expect(logged_in_page).to_have_url(f"{BASE_URL}/inventory.html")

    def test_cart_survives_navigation(self, logged_in_page: Page):
        """add item, click into detail, go back — badge should still show 1"""
        add_item(logged_in_page, BACKPACK_BTN)
        logged_in_page.locator(".inventory_item_name").first.click()
        logged_in_page.click("[data-test='back-to-products']")
        expect(
            logged_in_page.locator("[data-test='shopping-cart-badge']")
        ).to_have_text("1")

    def test_checkout_button_visible(self, logged_in_page: Page):
        go_to_cart(logged_in_page)
        expect(logged_in_page.locator("[data-test='checkout']")).to_be_visible()
