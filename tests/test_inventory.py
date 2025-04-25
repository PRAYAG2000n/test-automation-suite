import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL


class TestInventoryDisplay:

    def test_six_items_shown(self, logged_in_page: Page):
        expect(logged_in_page.locator(".inventory_item")).to_have_count(6)

    def test_items_have_names(self, logged_in_page: Page):
        names = logged_in_page.locator(".inventory_item_name")
        for i in range(6):
            expect(names.nth(i)).not_to_be_empty()

    def test_prices_have_dollar_sign(self, logged_in_page: Page):
        prices = logged_in_page.locator(".inventory_item_price")
        for i in range(6):
            txt = prices.nth(i).text_content()
            assert txt.startswith("$"), f"expected $ prefix, got: {txt}"

    def test_images_have_src(self, logged_in_page: Page):
        imgs = logged_in_page.locator(".inventory_item img")
        for i in range(imgs.count()):
            src = imgs.nth(i).get_attribute("src")
            assert src, "img tag has no src"


class TestSorting:

    def test_az(self, logged_in_page: Page):
        logged_in_page.select_option("[data-test='product-sort-container']", "az")
        first_name = logged_in_page.locator(".inventory_item_name").first
        expect(first_name).to_have_text("Sauce Labs Backpack")

    def test_za(self, logged_in_page: Page):
        logged_in_page.select_option("[data-test='product-sort-container']", "za")
        first_name = logged_in_page.locator(".inventory_item_name").first
        expect(first_name).to_have_text("Test.allTheThings() T-Shirt (Red)")

    def test_price_low_to_high(self, logged_in_page: Page):
        logged_in_page.select_option("[data-test='product-sort-container']", "lohi")
        price = logged_in_page.locator(".inventory_item_price").first.text_content()
        assert price == "$7.99"

    def test_price_high_to_low(self, logged_in_page: Page):
        logged_in_page.select_option("[data-test='product-sort-container']", "hilo")
        price = logged_in_page.locator(".inventory_item_price").first.text_content()
        assert price == "$49.99"


class TestItemDetail:

    def test_click_into_detail(self, logged_in_page: Page):
        logged_in_page.locator(".inventory_item_name").first.click()
        expect(logged_in_page.locator(".inventory_details_name")).to_be_visible()

    def test_back_to_products(self, logged_in_page: Page):
        logged_in_page.locator(".inventory_item_name").first.click()
        logged_in_page.click("[data-test='back-to-products']")
        expect(logged_in_page).to_have_url(f"{BASE_URL}/inventory.html")

    def test_add_to_cart_toggles_to_remove(self, logged_in_page: Page):
        logged_in_page.click("[data-test='add-to-cart-sauce-labs-backpack']")
        expect(
            logged_in_page.locator("[data-test='remove-sauce-labs-backpack']")
        ).to_be_visible()

    def test_burger_menu_opens(self, logged_in_page: Page):
        logged_in_page.click("#react-burger-menu-btn")
        expect(logged_in_page.locator(".bm-menu")).to_be_visible()
