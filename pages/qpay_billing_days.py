import os
import time
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import file_operations
from selenium_handler import SeleniumHelperPage


class QpayBillingDaysPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    import_type_dropdown = (By.ID, "ImportType")
    download_template_button = (By.ID, 'template')
    choose_file_button = (By.ID, 'BillableDaysUpload')
    import_button = (By.CSS_SELECTOR, "input[type='submit'][value='Import']")
    reset_button = (By.CSS_SELECTOR, 'img[alt="Reset"]')

    # ----------------------------------------------------------------------

    def select_import_type(self, import_type):
        try:
            self.wait_for_element(self.import_type_dropdown)
            select = Select(self.driver.find_element(*self.import_type_dropdown))
            select.select_by_visible_text(import_type)
            self.wait_for_page_load(self.driver)
            return True
        except (NoSuchElementException, TimeoutException):
            self.log.error("Failed to select {} from the import type list".format(import_type))
            return False

    def upload_file(self, file_path):
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            up_flag = file_operations.load_config_file(config_path, str('Input'), "UPLOAD_FLAG")
            input_location = file_operations.load_config_file(config_path, str('Input'), "INPUT_FILE_LOCATION")
            if up_flag == 'True':
                self.wait_for_element(self.choose_file_button)
                self.set_text(file_path, *self.choose_file_button)
                try:
                    self.driver.find_element(*self.import_button).is_enabled()
                    self.click(*self.import_button)
                    time.sleep(5)
                    # handler for incomplete upload file
                    if len(list(Path(os.path.join(os.getcwd(), input_location)).glob('*.txt'))) > 0:
                        return False
                    self.wait_for_page_load(self.driver)
                    self.wait_for_element(self.reset_button)
                    self.click(*self.reset_button)
                    self.log.info('Clicked on upload button')
                    self.wait_for_page_load(self.driver)
                    return True
                except InvalidElementStateException:
                    self.log.error("Unable to upload the file {}".format(file_path))
                    return False
            else:
                return True
        except (NoSuchElementException, TimeoutException):
            self.log.error("Function {} failed".format('upload_file'))
            return False

    def download_template(self, template_type):
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            download_flag = file_operations.load_config_file(config_path, str('Input'), "DOWNLOAD_FLAG")
            if download_flag == 'True':
                self.select_import_type(template_type)
                self.wait_for_element(self.download_template_button)
                self.click(*self.download_template_button)
                self.log.info("Clicked on download button")
                self.wait_for_page_load(self.driver)
                time.sleep(5)
            return True
        except (NoSuchElementException, TimeoutException):
            self.log.error("Function {} failed".format('download_template'))
            return False
