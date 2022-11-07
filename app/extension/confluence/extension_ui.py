import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates
from util.conf import CONFLUENCE_SETTINGS

""" TODO Add selenium actions for the following:
    View Compliance Profile Search
"""


def app_login_page(webdriver, datasets):
    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.wait_for_page_loaded()
            login_page.set_credentials(username=username, password=password)
            login_page.click_login_button()
            if login_page.is_first_login():
                login_page.first_user_setup()
            all_updates_page = AllUpdates(webdriver)
            all_updates_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()


def __check_tab_has_rendered(page, tab_name):
    page.wait_until_visible(By.XPATH, f"//div[text()='{tab_name}']")


def __check_h3_has_rendered(page, heading):
    page.wait_until_visible((By.XPATH, f"//h3[text()='{heading}']"))

def click_tab(webdriver, tab_name):
    tab = webdriver.find_element(By.XPATH, f"//div[text()='{tab_name}']")
    tab.click()


def click_tab_and_check_heading(page, webdriver, tab_name, heading):
    click_tab(webdriver, tab_name)
    page.wait_until_visible((By.XPATH, f"//h3[text()='{heading}']"))


def view_config_page(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_config_page")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/servlet/server-classification/classification")
        page.wait_until_visible((By.CLASS_NAME, "admin-heading"))
        # Check whether get started page has been rendered
        page.wait_until_visible((By.XPATH, "//h3[text()='Get Started']"))
        # Check whether all tabs are visible
        page.wait_until_visible((By.XPATH, "//div[text()=' Get Started ']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Classification Levels ']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Global Options']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Spaces']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Statistics']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Enforce Restrictions']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Optimizations']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Macro Options']"))
        page.wait_until_visible((By.XPATH, "//div[text()=' Bulk Change']"))



        @print_timing("selenium_compliance_view_config_page:classification_levels")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Classification Levels ", "Classification Levels")
        sub_measure()

        @print_timing("selenium_compliance_view_config_page:global_options")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Global Options", "Global Options")
        sub_measure()

        @print_timing("selenium_compliance_view_config_page:statistics")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Statistics", "Statistics")
        sub_measure()

    measure()


def view_space_page(webdriver, datasets):

    def get_random_space_key():
        random_page = random.choice(datasets["pages"])
        return random_page[1]

    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_space_page")
    def measure():
        space_key = get_random_space_key()
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/compliance/search.action?spaceKey={space_key}")
        # Check that search page has rendered by checking for export to csv button
        page.wait_until_visible((By.CLASS_NAME, "export-csv"))

        @print_timing("selenium_compliance_view_space_page:sensitive_data")
        def sub_measure():
            click_tab(webdriver, " Sensitive Data Search")
        sub_measure()

        @print_timing("selenium_compliance_view_space_page:statistics")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Statistics", "Statistics")
        sub_measure()

        @print_timing("selenium_compliance_view_space_page:space_settings")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Space Settings", "Space Settings")
        sub_measure()

    measure()


def view_global_search(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_global_search")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/servlet/server-classification/browse")
        # Check Classification Level Search Tab has rendered
        __check_tab_has_rendered(page, " Classification Level Search")
        # Check search bar has rendered
        page.wait_until_visible((By.CLASS_NAME, "top-search-bar"))
        click_tab(webdriver, " Sensitive Data Search")

        @print_timing("selenium_compliance_view_global_search:sensitive_data")
        def sub_measure():
            click_tab(webdriver, "Sensitive Data Search")
            # Check table has rendered
            page.wait_until_visible((By.CLASS_NAME, "tableContainerStyle"))


def view_detection_page(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_detection_page")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/servlet/server-classification/analysis")
        # Check get started page has rendered
        __check_h3_has_rendered(page, "Get Started")

        @print_timing("selenium_compliance_view_detection_page:extractions")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Extractions ", "Extractions")
        sub_measure()

        @print_timing("selenium_compliance_view_detection_page:scan_options")
        def sub_measure():
            click_tab_and_check_heading(page, webdriver, " Scan Options ", "Scan Options")
            # Check progress bar has rendered
            page.wait_until_visible((By.CLASS_NAME, "progress-bar-container"))

            # Check scan button has rendered
            page.wait_until_visible((By.CLASS_NAME, "scan-btn"))
        sub_measure()
    measure()


def view_automation_page(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_automation_page")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/servlet/server-classification/automation")
        # Check heading has rendered
        page.wait_until_visible((By.XPATH, "//h2[text()='Automation']"))

    measure()


def view_log_page(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_log_page")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/servlet/server-classification/audit")
        # Check heading has rendered
        __check_h3_has_rendered(page, "Action Log")

    measure()


def view_compliance_profile_tab(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_compliance_view_profile_tab")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/plugins/compliance/profile.action")
        page.wait_until_visible((By.CLASS_NAME, "top-search-bar"))
        page.wait_until_visible((By.CLASS_NAME, "export-csv"))


