#!/usr/bin/env python

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
import csv, json, os

today = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
save_path = "data/sewage.csv"
save_path_json = "data/sewage.json"
URL = f"https://riversandseaswatch.southernwater.co.uk/release-history?BathingSite=FOLKESTONE&StartDate={today}T00%3A00"


async def run_scrape(browser):
    # Create a fresh context each run
    context = await browser.new_context(accept_downloads=True)
    page = await context.new_page()

    try:
        print("Opening page…")
        await page.goto(URL, wait_until="networkidle")

        # Accept cookies if present
        try:
            await page.wait_for_selector("#onetrust-accept-btn-handler", timeout=5000)
            print("Accepting cookies…")
            await page.click("#onetrust-accept-btn-handler")
        except:
            pass

        # Wait for CSV button
        try:
            print("Waiting for Export CSV button…")
            await page.wait_for_selector("button:has-text('Export CSV')")
        except:
            print("No data available")
            with open(save_path_json, "w") as f:
                json.dump({"Message": "No releases"}, f, indent=2)
            return

        print("Clicking Export CSV Button")
        await page.click("button:has-text('Export CSV')")

        print("Waiting for Continue button…")
        continue_btn = page.get_by_role("button", name="Continue")
        await continue_btn.wait_for()

        print("Downloading CSV…")
        async with page.expect_download() as download_info:
            await continue_btn.click()

        download = await download_info.value
        await download.save_as(save_path)

        print("Converting to JSON")
        with open(save_path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))

        with open(save_path_json, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)

        os.remove(save_path)

    finally:
        # ALWAYS close context to avoid leaks
        await context.close()


async def main_loop():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        while True:
            print("Running sewage check…")
            await run_scrape(browser)
            print("Sleeping 30 minutes…")
            await asyncio.sleep(1800)


if __name__ == "__main__":
    asyncio.run(main_loop())
