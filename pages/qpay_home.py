from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from selenium_handler import SeleniumHelperPage


class QpayHomePage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    menu_list = (By.CSS_SELECTOR, ".navigation [class='menu'] [id^='menu_'] a")
    billing_days_link = (By.LINK_TEXT, "Billing Days")

    # ----------------------------------------------------------------------

    def select_qpay_report_type(self):
        prim_menu = None
        sec_menu = None
        try:
            self.wait_for_page_load(self.driver)
            elements = self.driver.find_elements(*self.menu_list)
            if len(elements) == 0:
                self.log.warning("{} primary menu does not have sub menus under it".format(prim_menu))
                return False
            prim_flag = False
            for ele in elements:
                prim_menu = ele.text.strip()
                if prim_menu == 'Magna Billing':
                    prim_flag = True
                    actions = ActionChains(self.driver)
                    actions.move_to_element(ele).perform()
                    # getting sub menu from primary menu
                    self.wait_for_element(self.billing_days_link)
                    self.click(*self.billing_days_link)
                    self.wait_for_page_load(self.driver)
                    return True
                    """for i in elements:
                        sec_menu = i.text.strip()
                        if sec_menu == 'Billing Days':
                            i.click()
                            self.wait_for_page_load(self.driver)
                            return True """
            if not prim_flag:
                return False
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
            self.log.erro('Failed to find the primary menu {} or secondary menu {}'.format(prim_menu, sec_menu))
            return False
