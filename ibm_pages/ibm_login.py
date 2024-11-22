from selenium.webdriver.common.by import By

from selenium_handler import SeleniumHelperPage


class IBMLoginPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    IBMId_text = (By.CSS_SELECTOR, "[id='username'][name='username']")
    continue_button = (By.CSS_SELECTOR, "[id='continue-button'][class^='submit-button']")
    password_text = (By.CSS_SELECTOR, "[id='password'][name='password']")
    error_label = (By.CSS_SELECTOR, "div#password-error-msg")
    login_button = (By.CSS_SELECTOR, "[id='signinbutton'][class^='submit-button']")
    # ----------------------------------------------------------------------
