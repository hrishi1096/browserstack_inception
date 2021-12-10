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

from time import sleep


GOOGLE_URL="https://www.google.com"
IMPLICIT_WAIT_TIME = 10
EXPLICIT_WAIT_TIME = 30
WAIT = 3
BSTACK_DEMO_AC_EMAIL = "hrishikesh.b+demo@browserstack.com"
BSTACK_DEMO_AC_PASSWD = "Demoaccount@123"
USERNAME = os.environ['BROWSERSTACK_USERNAME']
ACCESSKEY = os.environ['BROWSERSTACK_ACCESS_KEY']


capabilities = [{
        'os_version': '10',
        'os': 'Windows',
        'browser': 'firefox',
        'browser_version': '94.0',
        "browserstack.geoLocation": "IE",
        # "browserstack.local" : "true",
        'name': 'Firefox test',
        'build': 'Browserstack_inception_geoloc_IE'
    },
    {
        'os_version': 'Monterey',
        'os': 'OS X',
        'browser': 'safari',
        'browser_version': '15.0',
        "browserstack.geoLocation": "IE",
        # "browserstack.local" : "true",
        'name': 'Safari Test',
        'build': 'Browserstack_inception_geoloc_IE'
    },
    {
        'os_version': '11',
        'os': 'Windows',
        'browser': 'chrome',
        'browser_version': '96.0',
        "browserstack.geoLocation": "IE",
        # "browserstack.local" : "true",
        'name': 'Chrome Test',
        'build': 'Browserstack_inception_geoloc_IE'
}]



def init(desired_cap):
    driver = webdriver.Remote(
        command_executor='https://' + USERNAME + ':' + ACCESSKEY + '@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=desired_cap)
    driver.implicitly_wait(IMPLICIT_WAIT_TIME)
    driver.maximize_window()
    return driver

def cleanup(driver):
    driver.quit()

def get_element_with_xpath(driver, xpath):
    return WebDriverWait(driver, EXPLICIT_WAIT_TIME).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def get_element_with_css(driver, css):
    return WebDriverWait(driver, EXPLICIT_WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))


def bstack_inception(driver):
    # Go to google
    driver.get(GOOGLE_URL)

    # Hit "I agree" on the cookies banner
    get_element_with_xpath(driver, '//*[@id="L2AGLb"]/div').click()

    # Get the Google search box, type in the desired keyword and hit ENTER
    gsearch_box = get_element_with_css(driver, 'input[aria-label="Search"]')
    gsearch_box.send_keys("Browserstack")
    gsearch_box.send_keys(Keys.ENTER)
    sleep(WAIT)

    # Go to browserstack home page by clicking on the correct entry from google search results
    get_element_with_xpath(driver, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div[1]/a/h3').click()
    sleep(WAIT)

    # Click on "Sign in"
    get_element_with_xpath(driver, '//*[@id="primary-menu"]/li[5]/a').click()
    sleep(WAIT)
    # Enter the email id
    get_element_with_css(driver, 'input[id="user_email_login"]').send_keys(BSTACK_DEMO_AC_EMAIL)
    # Enter the password
    get_element_with_css(driver, 'input[id="user_password"]').send_keys(BSTACK_DEMO_AC_PASSWD)
    # Click submit
    get_element_with_css(driver, 'input[value="Sign me in"]').click()
    sleep(WAIT)

    # Click Windows 11 and then start a live session with Chrome
    get_element_with_css(driver, 'div[data-test-ositem="win11"]').click()
    get_element_with_css(driver, 'div[data-rbd-draggable-id="win11__chrome__96.0"]').click()
    # Longer wait time as a live session is being launched at this point
    sleep(WAIT * 7)

    # Wait until the stop session option is visible, it means that the session is launched
    # get_element_with_css(driver, 'div[id="stop-session"]')

    # Click 'got it' on the banner for self-signed certificate
    get_element_with_css(driver, 'button[class="spotlight__button"]').click()
    sleep(WAIT)

    # Close the banner for local testing (applicable for chrome only)
    # get_element_with_css(driver, '#skip-local-installation').click()

    # Switch to active element which gives control of the live session
    driver.switch_to.active_element.click()
    sleep(WAIT)
    # Hit Control + L which gives control of the URL bar
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('l').key_up(Keys.CONTROL).perform()
    sleep(WAIT)
    # Type google.com and git TAB so that the next keyword we enter will get searched for on Google
    ActionChains(driver).send_keys('google.com').key_down(Keys.TAB).key_up(Keys.TAB).perform()
    sleep(WAIT)
    # Type the keyword and hit ENTER
    ActionChains(driver).send_keys("Browserstack", Keys.ENTER).perform()
    sleep(WAIT)

    # Stop the live session
    get_element_with_css(driver, 'div[id="stop-session"]').click()

    return 1


def test_bstack_inception():
    # Setup
    for caps in capabilities:
        driver = init(caps)

        if (bstack_inception(driver)):
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": \
                {"status":"passed", "reason": "Browserstack inception successful!"}}')
        else:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": \
                {"status":"failed", "reason": "Browserstack inception unsuccessful"}}')

        # Cleanup
        cleanup(driver)




