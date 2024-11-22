from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from selenium_handler import SeleniumHelperPage


class QpayLoginPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    user_name_text = (By.CSS_SELECTOR, "[id='form-username'][name='UserName']")
    password_text = (By.CSS_SELECTOR, "[id='form-password'][name='Password']")
    submit_button = (By.CSS_SELECTOR, "[id='LoginId'][class='btnLogin']")
    error_label = (By.CSS_SELECTOR, "div.validation-summary-errors ul li")

    # ----------------------------------------------------------------------

    def qpay_login(self, login_id, pwd):
        try:
            self.wait_for_element(self.user_name_text)
            self.clear_text(*self.user_name_text)
            self.set_text(login_id, *self.user_name_text)
            self.wait_for_element(self.password_text)
            self.clear_text(*self.password_text)
            self.set_text(pwd, *self.password_text, flag=False)
            self.wait_for_element(self.submit_button)
            self.click(*self.submit_button)
            self.wait_for_page_load(self.driver)
            # check for login failures
            try:
                self.driver.find_element(*self.error_label).is_displayed()
                self.log.error("Unable to login to QPay")
                return False
            except NoSuchElementException:
                pass
            return True
        except (NoSuchElementException, TimeoutException):
            self.log.error("Failed to login to Qpay")
            return False
