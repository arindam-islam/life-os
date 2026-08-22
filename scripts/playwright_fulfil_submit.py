#!/usr/bin/env python3
"""
Playwright Visible (Headful) Web Application Auto-Filler for Fulfil.io (JOB-FULFIL-001)
Navigates: jobs.fulfil.io -> Product Consultant Job -> Apply (/c/new),
fills candidate name, email, phone, uploads compiled PDF resume & cover letter,
and pauses at the review screen for you to watch live on your Mac screen!
"""

import os
import sys
import json
import time

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUME_PDF_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "pdf_assets", "Arindam_Islam_Resume_Fulfil.pdf")
COVER_LETTER_PDF_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "pdf_assets", "Arindam_Islam_Cover_Letter_Fulfil.pdf")
PROOF_SCREENSHOT_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "pdf_assets", "fulfil_form_filled_proof.png")

BASE_URL = "https://jobs.fulfil.io/"


def run_submission():
    from playwright.sync_api import sync_playwright

    print(f"🖥️ Launching VISIBLE Chrome browser window on your Mac desktop...")
    print(f"   Base URL: {BASE_URL}")
    print(f"   Resume PDF: {RESUME_PDF_PATH}")
    print(f"   Cover Letter PDF: {COVER_LETTER_PDF_PATH}")

    with sync_playwright() as p:
        # Launch visible browser window
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Step 1: Open landing page
        page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
        print("✅ 1. Navigated to Fulfil Careers homepage.")
        time.sleep(2)

        # Step 2: Click job title link
        job_link = page.locator("a[href*='product-consultant-associate-supply-chain']").first
        if job_link.count() > 0:
            print(f"✅ 2. Clicking job posting: '{job_link.inner_text()}'")
            job_link.click()
            page.wait_for_load_state("networkidle")
            time.sleep(2)

        # Step 3: Click Apply button
        apply_btn = page.locator("a[href*='/apply'], button:has-text('Apply'), a:has-text('Apply')").first
        if apply_btn.count() > 0:
            print(f"✅ 3. Clicking Apply button: '{apply_btn.inner_text()}'")
            apply_btn.click()
            page.wait_for_load_state("networkidle")
            time.sleep(2)

        print(f"📍 Current Form URL: {page.url}")

        # Step 4: Fill candidate information
        if page.locator("input[name='candidate.name']").is_visible():
            page.fill("input[name='candidate.name']", "Arindam Islam")
            print("  • Filled Name: Arindam Islam")

        if page.locator("input[name='candidate.email']").is_visible():
            page.fill("input[name='candidate.email']", "arindambevan04@gmail.com")
            print("  • Filled Email: arindambevan04@gmail.com")

        if page.locator("input[name='candidate.phone']").is_visible():
            page.fill("input[name='candidate.phone']", "+918553775736")
            print("  • Filled Phone: +918553775736")

        # Step 5: Attach PDF Resume & Cover Letter
        cv_input = page.locator("input[name='candidate.cv']")
        if cv_input.count() > 0 and os.path.exists(RESUME_PDF_PATH):
            cv_input.set_input_files(RESUME_PDF_PATH)
            print("  • Attached Resume PDF: Arindam_Islam_Resume_Fulfil.pdf")

        cl_input = page.locator("input[name='candidate.coverLetterFile']")
        if cl_input.count() > 0 and os.path.exists(COVER_LETTER_PDF_PATH):
            cl_input.set_input_files(COVER_LETTER_PDF_PATH)
            print("  • Attached Cover Letter PDF: Arindam_Islam_Cover_Letter_Fulfil.pdf")

        time.sleep(3)

        # Scroll to submit button and take screenshot proof
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        page.screenshot(path=PROOF_SCREENSHOT_PATH, full_page=True)

        print("\n👀 FORM FILLED & PAUSED AT FINAL REVIEW SCREEN!")
        print("   The Chrome window is open on your screen right now.")
        print("   Verify the filled fields, uploaded PDFs, and click Submit whenever you are ready.")
        print("   Keeping browser open for 90 seconds so you can watch live...\n")

        time.sleep(90)
        browser.close()

    return PROOF_SCREENSHOT_PATH


def main():
    run_submission()


if __name__ == "__main__":
    main()
