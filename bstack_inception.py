import sys
import os
# To run from the terminal
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from browserstack.local import Local
import pytest
from time import sleep


GOOGLE_URL="https://www.google.com"
IMPLICIT_WAIT_TIME = 10
EXPLICIT_WAIT_TIME = 30
WAIT = 3
BSTACK_DEMO_AC_EMAIL = "hrishikesh.b+demo@browserstack.com"
BSTACK_DEMO_AC_PASSWD = "Demoaccount@123"
USERNAME = os.environ['BROWSERSTACK_USERNAME']
ACCESSKEY = os.environ['BROWSERSTACK_ACCESS_KEY']
IDENTIFIER = os.environ['BROWSERSTACK_LOCAL_IDENTIFIER']

capabilities = [
    {
        'os_version': '10',
        'os': 'Windows',
        'browser': 'firefox',
        'browser_version': '94.0',
        'name': 'Firefox test',
        'build': IDENTIFIER,
        'project': 'Technical assignment',
        "browserstack.local" : "true",
        "browserstack.selenium_version" : "3.141.59",
        "browserstack.console" : "verbose",
        "browserstack.networkLogs" : "true",
        "browserstack.maskCommands" : "setValues"
    },
    {
        'os_version': 'Monterey',
        'os': 'OS X',
        'browser': 'safari',
        'browser_version': '15.0',
        'name': 'Safari Test',
        'build': IDENTIFIER,
        'project': 'Technical assignment',
        "browserstack.local" : "true",
        "browserstack.selenium_version" : "3.141.59",
        "browserstack.console" : "verbose",
        "browserstack.networkLogs" : "true",
        "browserstack.maskCommands" : "setValues"
    },
    {
        'os_version': '11',
        'os': 'Windows',
        'browser': 'chrome',
        'browser_version': '96.0',
        'name': 'Chrome Test',
        'build': IDENTIFIER,
        'project': 'Technical assignment',
        "browserstack.local" : "true",
        "browserstack.selenium_version" : "3.141.59",
        "browserstack.console" : "verbose",
        "browserstack.networkLogs" : "true",
        "browserstack.maskCommands" : "setValues"
    }
]


class TestClass():
    def setup_class(self):
        # Code bindings for starting Browserstack Local with `--force-local` flag
        self.bs_local = Local()
        self.bs_local_args = {"key": ACCESSKEY, "forcelocal": "true"}
        self.bs_local.start(**self.bs_local_args)

    def teardown_class(self):
        self.bs_local.stop()

    def setup_method(self):
        self.test_successful = False

    def teardown_method(self):
        if self.test_successful:
            self.driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": \
                {"status":"passed", "reason": "Browserstack inception successful!"}}')
        else:
            self.driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": \
                {"status":"failed", "reason": "Browserstack inception unsuccessful"}}')
        self.driver.quit()

    # Some helper functions
    def get_element_with_xpath(self, xpath):
        return WebDriverWait(self.driver, EXPLICIT_WAIT_TIME).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def get_element_with_css(self, css):
        return WebDriverWait(self.driver, EXPLICIT_WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))

    # Inception
    @pytest.mark.parametrize('desired_cap', capabilities)
    def test_bstack_inception(self, desired_cap):
        self.driver = webdriver.Remote(
            command_executor='https://' + USERNAME + ':' + ACCESSKEY + '@hub-cloud.browserstack.com/wd/hub',
            desired_capabilities=desired_cap)
        self.driver.implicitly_wait(IMPLICIT_WAIT_TIME)
        self.driver.maximize_window()

        # Go to google
        self.driver.get(GOOGLE_URL)

        # Hit "I agree" on the cookies banner
        self.get_element_with_xpath('//div[contains(text(), "I agree")]').click()

        # Get the Google search box, type in the desired keyword and hit ENTER
        gsearch_box = self.get_element_with_css('input[aria-label="Search"]')
        gsearch_box.send_keys("Browserstack")
        gsearch_box.send_keys(Keys.ENTER)
        sleep(WAIT)

        # Go to browserstack home page by clicking on the correct entry from google search results
        self.get_element_with_xpath('//h3[contains(text(), "BrowserStack: Most")]').click()
        sleep(WAIT)

        # Click on "Sign in"
        self.get_element_with_xpath('//*[@id="primary-menu"]/li[5]/a').click()
        sleep(WAIT)

        # Enter the email id
        self.get_element_with_css('input[id="user_email_login"]').send_keys(BSTACK_DEMO_AC_EMAIL)
        # Enter the password
        self.get_element_with_css('input[id="user_password"]').send_keys(BSTACK_DEMO_AC_PASSWD)
        # Click submit
        self.get_element_with_css('input[value="Sign me in"]').click()
        sleep(WAIT)

        # Click on Live
        self.get_element_with_xpath('//a[@class="header__product-name"][contains(text(), Live)]').click()
        sleep(WAIT)

        # Click Windows 11 and then start a live session with Chrome
        self.get_element_with_css('div[data-test-ositem="win11"]').click()
        self.get_element_with_css('div[data-rbd-draggable-id="win11__chrome__96.0"]').click()
        # Longer wait time as a live session is being launched at this point
        sleep(WAIT * 7)

        # Wait until the stop session option is visible, it means that the session is launched
        # get_element_with_css(driver, 'div[id="stop-session"]')

        # Click 'got it' on the banner for self-signed certificate
        self.get_element_with_css('button[class="spotlight__button"]').click()
        sleep(WAIT)

        # Close the banner for local testing (applicable for chrome only)
        # get_element_with_css(driver, '#skip-local-installation').click()

        # Switch to active element which gives control of the live session
        self.driver.switch_to.active_element.click()
        sleep(WAIT)
        # Hit Control + L which gives control of the URL bar
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('l').key_up(Keys.CONTROL).perform()
        sleep(WAIT)
        # Type google.com and git TAB so that the next keyword we enter will get searched for on Google
        ActionChains(self.driver).send_keys('google.com').key_down(Keys.TAB).key_up(Keys.TAB).perform()
        sleep(WAIT)
        # Type the keyword and hit ENTER
        ActionChains(self.driver).send_keys("Browserstack", Keys.ENTER).perform()
        sleep(WAIT)

        # Stop the live session
        self.get_element_with_css('div[id="stop-session"]').click()

        # Status update
        self.test_successful = True







