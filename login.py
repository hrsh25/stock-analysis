import json
import pyotp
from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import parse_qs, urlparse
from auth import generate


def run(playwright: Playwright):
    f = open('./config.json', "r+")
    config = json.load(f)
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    with page.expect_request(f"*{config['request_url']}code*") as request:
        page.goto(config['login_url'])
        page.locator("#mobileNum").fill(config['mobile_number'])
        page.locator("#mobileNum").press("Enter")
        page.locator("#otpNum").fill(pyotp.TOTP(config['totp_key']).now())
        page.get_by_role("button", name="Continue").click()
        page.get_by_label("Enter 6-digit PIN").fill(config['pin'])
        page.get_by_label("Enter 6-digit PIN").press("Enter")
        page.wait_for_load_state()

    url = request.value.url
    parsed = urlparse(url)
    code = parse_qs(parsed.query)['code'][0]
    context.close()
    browser.close()
    generate(code)
    

def login():
    with sync_playwright() as playwright:
        run(playwright)

login()
