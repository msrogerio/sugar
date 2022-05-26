import platform, os
from selenium.webdriver.firefox.options import Options as  FirefoxOptions #Configuration Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Normal1994#@localhost/sugar'
SQLALCHEMY_TRACK_MODIFICATIONS = False

def setUpFirefox():
    global driver_firefox
    options = FirefoxOptions()
    options.headless = False
    # options.headless = True

    if platform.system() == 'Darwin':
        profile = FirefoxProfile('/Users/marlonrogerio/Library/Application Support/Firefox/Profiles/f9citt77.default-release')
        profile.set_preference("security.fileuri.strict_origin_policy", False)
        profile.set_preference("dom.disable_beforeunload", True)
        profile.set_preference("browser.tabs.warnOnClose", True)
        profile.set_preference("browser.privatebrowsing.autostart", True)
        profile.update_preferences()
        driver_firefox = webdriver.Firefox(
            executable_path='./mac/geckodriver',
            options=options,
            firefox_profile=profile,
            )
        return driver_firefox
    
    if platform.system() == 'Linux':
        driver_firefox = webdriver.Firefox(
            executable_path='./linux/geckodriver',
            options=options,
            firefox_profile=profile,
            )
        return driver_firefox

