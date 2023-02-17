from typing import Union

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class SeleniumDriver:
    def __init__(self, driver_type='chrome', headless=False, driver=None, driver_path=None):
        self.driver_type = driver_type
        self.headless = headless
        self.options = None
        self.driver = driver
        self.driver_path = driver_path

    def add_options(self, *options):
        """Add option to webdriver"""
        if self.options is None:
            self.set_options()

        for option in options:
            self.options.add_argument(option)

    def set_options(self):
        """Set options for the web driver based on the driver type"""
        if not self.options:
            if self.driver_type == 'chrome':
                self.options = ChromeOptions()
            elif self.driver_type == 'firefox':
                self.options = FirefoxOptions()
            else:
                raise ValueError(
                    f'Invalid driver type: {self.driver_type}. There are two options: "firefox" and "chrome." ')

    def set_driver(self):
        """Create the web driver based on the driver type and options"""
        if self.driver_type == 'chrome':
            self.driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=self.options)
        elif self.driver_type == 'firefox':
            self.driver = webdriver.Firefox(service=Service(
                GeckoDriverManager().install()), options=self.options)
        else:
            raise ValueError(f'Invalid driver type: {self.driver_type}')

    def get_driver(self) -> \
            Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]:
        """Return the web driver"""
        return self.driver

    def get_options(self):
        """Return the web driver options"""
        return self.options

    def setup(self):
        """Set up the web driver based on the user's requirements"""
        if self.options is None:
            self.set_options()
        self.set_driver()
        return self
