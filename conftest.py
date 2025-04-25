import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()

BASE_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
USERS = {
    "standard": {
        "username": os.getenv("STANDARD_USER", "standard_user"),
        "password": os.getenv("STANDARD_PASS", "secret_sauce"),
    },
    "locked": {
        "username": os.getenv("LOCKED_USER", "locked_out_user"),
        "password": os.getenv("LOCKED_PASS", "secret_sauce"),
    },
    "problem": {
        "username": os.getenv("PROBLEM_USER", "problem_user"),
        "password": os.getenv("PROBLEM_PASS", "secret_sauce"),
    },
    "perf": {
        "username": os.getenv("PERF_USER", "performance_glitch_user"),
        "password": os.getenv("PERF_PASS", "secret_sauce"),
    },
}


def do_login(page: Page, user_key="standard"):
    u = USERS[user_key]
    page.goto(BASE_URL)
    page.fill("[data-test='username']", u["username"])
    page.fill("[data-test='password']", u["password"])
    page.click("[data-test='login-button']")


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    do_login(page)
    page.wait_for_url("**/inventory.html", timeout=5000)
    return page
