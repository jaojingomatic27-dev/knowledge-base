# -*- coding: utf-8 -*-
"""Use Playwright to screenshot the HTML cheatsheets as clean PNG files."""
import os
from playwright.sync_api import sync_playwright

html_dir = r"C:\AI\cc\pvinverter\output"
files = {
    "_cheatsheet1.html": "solution_engineer_cheatsheet.png",
    "_cheatsheet2.html": "sales_vs_presales_cheatsheet.png",
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for html_file, png_file in files.items():
        page = browser.new_page(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
        page.goto("file:///" + os.path.join(html_dir, html_file).replace("\\", "/"))
        # get the actual content height
        content_height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": 1080, "height": max(1440, content_height + 100)})
        page.screenshot(path=os.path.join(html_dir, png_file), full_page=True)
        print(f"Done: {png_file}  (viewport height: {max(1080, content_height + 100)})")
    browser.close()

print("All screenshots saved.")
