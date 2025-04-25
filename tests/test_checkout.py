import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL

# reuse across tests
FNAME = "John"
LNAME = "Doe"
ZIPCODE = "10001"

def add_backpack_and_go_to_checkout(page: Page):
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("[data-test='shopping-cart-link']")
    page.click("[data-test='checkout']")


def fill_checkout_info(page: Page, first=FNAME, last=LNAME, zipcode=ZIPCODE):
    if first:
        page.fill("[data-test='firstName']", first)
    if last:
        page.fill("[data-test='lastName']", last)
    if zipcode:
        page.fill("[data-test='postalCode']", zipcode)
    page.click("[data-test='continue']")


class TestCheckoutStepOne:

    def test_info_page_loads(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        expect(logged_in_page.locator(".title")).to_have_text("Checkout: Your Information")

    def test_continue_to_overview(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        expect(logged_in_page.locator(".title")).to_have_text("Checkout: Overview")

    def test_missing_first_name(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        page = logged_in_page
        page.fill("[data-test='lastName']", LNAME)
        page.fill("[data-test='postalCode']", ZIPCODE)
        page.click("[data-test='continue']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_missing_last_name(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        page = logged_in_page
        page.fill("[data-test='firstName']", FNAME)
        page.fill("[data-test='postalCode']", ZIPCODE)
        page.click("[data-test='continue']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_missing_zip(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        page = logged_in_page
        page.fill("[data-test='firstName']", FNAME)
        page.fill("[data-test='lastName']", LNAME)
        page.click("[data-test='continue']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_cancel_goes_back_to_cart(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        logged_in_page.click("[data-test='cancel']")
        expect(logged_in_page).to_have_url(f"{BASE_URL}/cart.html")


class TestCheckoutOverview:
    def test_item_name_on_overview(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        expect(logged_in_page.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")

    def test_subtotal(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        expect(logged_in_page.locator("[data-test='subtotal-label']")).to_contain_text("$29.99")

    def test_tax_shown(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        expect(logged_in_page.locator("[data-test='tax-label']")).to_be_visible()

    def test_cancel_on_overview_goes_to_inventory(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        logged_in_page.click("[data-test='cancel']")
        expect(logged_in_page).to_have_url(f"{BASE_URL}/inventory.html")

    def test_multiple_items_on_overview(self, logged_in_page: Page):
        logged_in_page.click("[data-test='add-to-cart-sauce-labs-backpack']")
        logged_in_page.click("[data-test='add-to-cart-sauce-labs-bike-light']")
        logged_in_page.click("[data-test='shopping-cart-link']")
        logged_in_page.click("[data-test='checkout']")
        fill_checkout_info(logged_in_page)
        expect(logged_in_page.locator(".cart_item")).to_have_count(2)


class TestOrderComplete:
    def test_finish_shows_thank_you(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        logged_in_page.click("[data-test='finish']")
        expect(logged_in_page.locator(".complete-header")).to_have_text("Thank you for your order!")

    def test_back_home_after_order(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        logged_in_page.click("[data-test='finish']")
        logged_in_page.click("[data-test='back-to-products']")
        expect(logged_in_page).to_have_url(f"{BASE_URL}/inventory.html")

    def test_pony_express_image(self, logged_in_page: Page):
        add_backpack_and_go_to_checkout(logged_in_page)
        fill_checkout_info(logged_in_page)
        logged_in_page.click("[data-test='finish']")
        expect(logged_in_page.locator(".pony_express")).to_be_visible()

    def test_empty_cart_checkout(self, logged_in_page: Page):
        """go straight to checkout without adding anything"""
        logged_in_page.click("[data-test='shopping-cart-link']")
        logged_in_page.click("[data-test='checkout']")
        fill_checkout_info(logged_in_page)
        expect(logged_in_page.locator(".cart_item")).to_have_count(0)  #overview should have zero items
