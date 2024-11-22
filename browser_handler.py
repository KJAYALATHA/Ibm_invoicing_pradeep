import os
import platform
import time

from get_chrome_driver import GetChromeDriver
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from file_handler import load_config_file, create_folder
from log_handler import custom_logger

log = custom_logger()
config_path = os.path.join(os.getcwd(), "config.cfg")
fold_name = load_config_file(config_path, str('Input'), "INPUT_FILE_LOCATION")
create_folder(os.path.join(os.getcwd(), fold_name))
download_dir = os.path.join(os.getcwd(), fold_name) + "\\"
headless_flag = load_config_file(config_path, str('Browser'), "HEADLESS")
err_msg = 'No such driver, error: {} while getting driver type specified'


def get_driver(browser):
    """
    method to get the type of browser
    :param browser: options are [chrome | chrome_headless |firefox | firefox_headless | edge]
    :return: driver object
    """
    driver = None
    try:
        if browser.lower() == "chrome":
            driver = get_chrome()
        elif browser.lower() == 'edge':
            driver = get_edge()
    except WebDriverException as wde:
        log.error('No such driver, error: {} while getting driver type specified'.format(wde.msg))
        return None
    return driver


def get_chrome():
    """
    method to get the chrome driver with options and capabilities
    :return: webdriver
    """
    chrome_options = None
    try:
        # below settings are for setting default download path for automatic downloads.
        prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.default_directory": str(download_dir)
        }
        chrome_options = webdriver.ChromeOptions()
        if headless_flag == "True":
            chrome_options.add_argument('--headless')
        # start browser in maximize based on OS
        if platform.system().lower() == "windows":
            chrome_options.add_argument('--start-maximized')
        else:
            chrome_options.add_argument('--kiosk')
        chrome_options.add_argument("--no-sandbox")
        # to disable chrome notifications
        chrome_options.add_argument("--disable-notifications")
        # disable chrome automatic upgrade
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.page_load_strategy = 'normal'
        driver = webdriver.Chrome(options=chrome_options)
        log.info('initiated chrome driver with web driver-manager, options')
    except (SessionNotCreatedException, ValueError, TypeError, AttributeError):
        chrome_ver = GetChromeDriver()
        chrome_ver.auto_download(output_path=os.path.join(os.getcwd(), "drivers"), extract=True)
        chrome_driver_path = Service(os.path.join(os.getcwd(), "drivers", "chromedriver.exe"))
        driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)
    return driver


def get_edge():
    """
    method to get the edge driver with options and capabilities
    :return: webdriver
    """
    try:
        # below settings are for setting default download path for automatic downloads.
        prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.default_directory": str(download_dir)
        }
        edge_options = webdriver.EdgeOptions()
        if headless_flag == "True":
            edge_options.add_argument('--headless')
        # start browser in maximize based on OS
        if platform.system().lower() == "windows":
            edge_options.add_argument('--start-maximized')
        else:
            edge_options.add_argument('--kiosk')
        edge_options.add_argument("--no-sandbox")
        # to disable chrome notifications
        edge_options.add_argument("--disable-notifications")
        # disable chrome automatic upgrade
        edge_options.add_argument("--disable-gpu")
        edge_options.add_experimental_option('prefs', prefs)
        edge_options.page_load_strategy = 'normal'
        # Clear browser data (optional)
        edge_options.add_argument('--delete-profile=Default')
        # Disable personalized web experiences
        edge_options.add_argument('--disable-features=msHoldTabToSearch,WebComponentsV0Enabled')
        edge_options.add_argument('--disable-features=msToASCIILowerEnabled')
        driver = webdriver.Edge(options=edge_options)
        log.info('initiated edge driver with web driver-manager, options')
    except WebDriverException as wde:
        log.error('No such driver, error: {} while getting driver type specified'.format(wde.msg))
        return None
    return driver


def enable_download_in_headless_chrome(driver, dwn_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': dwn_dir}}
    driver.execute("send_command", params)


def get_browser(browser, url):
    """
    method to get the browser and return the driver to calling test
    :param browser: type [chrome | headless]
    :param url: url to launch the application
    :return: driver to calling test
    """
    try:
        while close_all_browsers():
            time.sleep(1)
        web_driver = get_driver(browser)
        if web_driver is not None:
            time.sleep(3)
            if headless_flag == 'True':
                enable_download_in_headless_chrome(web_driver, download_dir)
            web_driver.get(url)
        else:
            log.error("Failed to initialize the chrome web driver")
            exit(-1)
        return web_driver
    except Exception as ex:
        log.error("Function get_browser failed with error :{}".format(ex))


def close_all_browsers():
    """
    method to kill any open firefox browsers
    :return: none
    """
    try:
        for browser_type in ["chromedriver", "chrome"]:
            if platform.system().startswith("Win"):
                os.system("taskkill /im {}.exe /f 2>NUL".format(browser_type))
            elif platform.system() in ["Linux", "Darwin"]:
                os.system("pkill {}.exe".format(browser_type))
    except OSError:
        pass
