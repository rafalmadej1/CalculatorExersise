"""Playwright end-to-end tests for the AGH Informatics Faculty website."""

from typing import NamedTuple

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect


def test_open_agh_website(page: Page):
    """Open the AGH Informatics Faculty website and verify the page title is not empty."""
    page.goto("https://www.informatyka.agh.edu.pl/pl/")

    print(page.title())

    assert page.title() != ""


def test_open_department_page(page: Page):
    """Test to navigate to the department page and verify the URL."""
    # Main page URL
    page.goto("https://www.informatyka.agh.edu.pl/pl/")
    print(page.title())

    # Department page URL
    page.get_by_role("link", name="Wydział", exact=True).click()
    #
    # expect(page.get_by_text("O Wydziale")).to_be_visible()
    page.get_by_role("link", name="O WYDZIALE").click()
    expect(page).to_have_url(
        "https://www.informatyka.agh.edu.pl/pl/wydzial/o-wydziale/"
    )
    expect(page.get_by_role("heading", name="O WYDZIALE")).to_be_visible()


def close_cookies_popup(page: Page):
    """Helper function to close the cookies popup if it is visible."""
    dialog = page.locator("#CookieModal")
    try:
        dialog.wait_for(state="visible", timeout=3000)
        print("Cookies popup is visible. Attempting to close it.")
        dialog.get_by_role("button", name="Akceptuję").click()
        expect(dialog).to_be_hidden()
        print("Cookies popup is now hidden.")
    except PlaywrightTimeoutError:
        print("Cookies popup did not appear within the timeout period.")


def test_postgraduate_studies(page: Page):
    """Test to navigate through the postgraduate studies section."""
    # Main page URL
    page.goto("https://www.informatyka.agh.edu.pl/pl/")
    expect(page).to_have_title("Strona główna | Wydział Informatyki AGH")
    page.get_by_role("link", name="Studia podyplomowe", exact=True).click()

    # Verify the URL of the postgraduate studies page
    expect(page).to_have_url("https://podyplomowe.informatyka.agh.edu.pl/")
    print(page.title())

    # Check if the cookies popup is visible and close it if it is
    close_cookies_popup(page)

    # Verify the URL of the postgraduate studies page
    page.get_by_role("link", name="Inżynieria systemów sztucznej").click()
    expect(page).to_have_url(
        "https://podyplomowe.informatyka.agh.edu.pl/oferta/sp-iissi/"
    )
    expect(
        page.get_by_role("heading", name="Inżynieria systemów sztucznej")
    ).to_be_visible()


class UrlChangeCase(NamedTuple):
    """Parameters for a single URL-change navigation test case."""

    start_url: str
    link_name: str
    exact: bool
    expected_url: str
    needs_cookies_close: bool


@pytest.mark.parametrize(
    "case",
    [
        UrlChangeCase(
            start_url="https://www.informatyka.agh.edu.pl/pl/",
            link_name="Studia podyplomowe",
            exact=True,
            expected_url="https://podyplomowe.informatyka.agh.edu.pl/",
            needs_cookies_close=False,
        ),
        UrlChangeCase(
            start_url="https://podyplomowe.informatyka.agh.edu.pl/",
            link_name="Inżynieria systemów sztucznej",
            exact=False,
            expected_url="https://podyplomowe.informatyka.agh.edu.pl/oferta/sp-iissi/",
            needs_cookies_close=True,
        ),
    ],
    ids=["studia_podyplomowe", "oferta_sp_iissi"],
)
def test_url_change(page: Page, case: UrlChangeCase):
    """Test that navigating from start_url via link_name changes the URL to expected_url."""
    page.goto(case.start_url)
    initial_url = page.url

    if case.needs_cookies_close:
        close_cookies_popup(page)

    page.get_by_role("link", name=case.link_name, exact=case.exact).click()
    expect(page).to_have_url(case.expected_url)

    assert (
        initial_url != page.url
    ), f"URL did not change. Initial: {initial_url}, Current: {page.url}"
