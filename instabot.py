import logging
from logging import Logger
from time import sleep
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium_handler import SeleniumDriver

import config
import constants
from selenium_handler import SeleniumDriver


class InstaBot:
    '''
    A simple instagram automation tool
    current features:
        - Sending personal messages to users
        - Searching hashtags and adding Like & comment on posts
    '''

    def __init__(self,
                 logger: Logger = None,
                 driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge] = None) -> None:
        self.logger = logger or self.get_logger()
        self.driver = driver or self.get_driver()

    def login(self) -> None:
        '''
        Log In user
        '''
        username = self.driver.find_element(
            By.NAME, config.INSTA_USERNAME_FIELD)
        password = self.driver.find_element(
            By.NAME, config.INSTA_PASSWORD_FIELD)
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, config.INSTA_SUBMIT_BUTTON)

        # Log into account
        username.click()
        for letter in list(constants.INSTA_USERNAME):
            username.send_keys(letter)
            sleep(0.2)
        sleep(2)
        password.click()
        for letter in list(constants.INSTA_PASSWORD):
            password.send_keys(letter)
            sleep(0.3)
        sleep(1)
        actions = ActionChains(self.driver)
        actions.move_to_element(submit_button)
        actions.click(submit_button)
        actions.perform()
        sleep(15)
        self.close_popups()

    def _search_item(self, query) -> None:
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, config.INSTA_SEARCH_BUTTON)
        search_button.click()
        sleep(5)

        search_input = self.driver.find_element(
            By.CSS_SELECTOR, config.INSTA_SEARCH_INPUT)
        search_input.send_keys(query)
        sleep(5)
        search_item = config.INSTA_SEARCH_ITEM.format(
            query=query
        )
        print(f"\n Search Item: {search_item} \n")
        self.driver.find_element(
            By.XPATH, search_item).click()
        sleep(5)
        self.close_popups()

    def _send_message(self, message=None) -> None:

        if message is None:
            message = constants.INSTA_MESSAGE_TO_SEND

        message_input_box = self.driver.find_element(
            By.CSS_SELECTOR, config.INSTA_MESSAGE_BOX)
        message_input_box.send_keys(message)
        sleep(2)
        message_input_box.send_keys(Keys.ENTER)
        sleep(2)

    def send_personal_messages(self) -> None:
        '''
        Send personal messages to each user from `INSTA_USERNAMES`
        '''
        self.login()
        # send message to a user
        for username in constants.INSTA_USERNAMES:
            self._search_item(username)

            try:
                self.driver.find_element(
                    By.XPATH, config.INSTA_PROFILE_MESSAGE_BUTTON).click()
                sleep(5)
                self.close_popups()
                self._send_message()
            except NoSuchElementException as e:
                print(
                    f"You're not following {username} or they've not accepted your request")
                self.logger.error(e)
                pass

    def _like_post(self) -> None:
        svg_button = self.driver.find_element(
            By.CSS_SELECTOR, config.INSTA_LIKE_SVG)
        svg_button.find_element(
            By.XPATH, config.INSTA_RELATIVE_BUTTON).click()
        sleep(1)

    def _comment_post(self, comment=None) -> None:
        def cbox():
            '''
            Small method to get updated element and
            solve this exception `selenium.common.exceptions.StaleElementReferenceException`
            '''
            return self.driver.find_element(
                By.CSS_SELECTOR, config.INSTA_COMMENT_BOX)
        if comment is None:
            comment = constants.INSTA_DEFAULT_COMMENT

        comment_box = cbox()
        comment_box.click()
        sleep(2)
        comment_box = cbox()
        comment_box.send_keys(comment)
        sleep(2)
        comment_box = cbox()
        comment_box.send_keys(Keys.ENTER)
        sleep(2)

    def comment_hashtag_posts(self):
        '''
        Comment on popular posts of provided hashtag
        '''
        self.login()
        self.close_popups()
        for tag in constants.INSTA_HASHTAGS:
            self._search_item(tag)
            post_list = self.driver.find_elements(
                By.CSS_SELECTOR, config.INSTA_HASHTAG_POST_LIST)

            for element in post_list[:constants.INSTA_POST_COMMENT_COUNT]:
                element.click()
                sleep(4)
                self._comment_post()
                sleep(2)
                self.driver.find_element(
                    By.CSS_SELECTOR, config.INSTA_CLOSE_BUTTON).click()
                sleep(1)

    def like_and_comment_hashtag_posts(self):
        '''
        Comment & Like on popular posts of provided hashtag
        '''
        self.login()
        self.close_popups()
        for tag in constants.INSTA_HASHTAGS:
            self._search_item(tag)
            post_list = self.driver.find_elements(
                By.CSS_SELECTOR, config.INSTA_HASHTAG_POST_LIST)

            for element in post_list[:constants.INSTA_POST_COMMENT_AND_LIKE_COUNT]:
                element.click()
                sleep(4)
                self._like_post()
                sleep(2)
                self._comment_post()
                sleep(2)
                self.driver.find_element(
                    By.CSS_SELECTOR, config.INSTA_CLOSE_BUTTON).click()
                sleep(1)

    def like_hashtag_posts(self):
        '''
        Like on popular posts of provided hashtag
        '''
        self.login()
        self.close_popups()

        for tag in constants.INSTA_HASHTAGS:
            self._search_item(tag)
            post_list = self.driver.find_elements(
                By.CSS_SELECTOR, config.INSTA_HASHTAG_POST_LIST)

            for element in post_list[:constants.INSTA_POST_LIKE_COUNT]:
                element.click()
                sleep(4)
                self._like_post()
                self.driver.find_element(
                    By.CSS_SELECTOR, config.INSTA_CLOSE_BUTTON).click()
                sleep(1)

    def close_popups(self) -> None:
        '''
        Close "Save Info" & "Turn Notification On" popups
        '''
        try:
            save_info = self.driver.find_element(
                By.XPATH, config.INSTA_NOT_NOW_BUTTON)
            save_info.click()
        except NoSuchElementException as e:
            self.logger.error(e)
            try:
                save_info = self.driver.find_element(
                    By.XPATH, config.INSTA_NOT_NOW_BUTTON)
                save_info.click()
            except NoSuchElementException as e:
                self.logger.error(e)

        try:
            turn_notification = self.driver.find_element(
                By.XPATH, config.INSTA_NOT_NOW_BUTTON)
            turn_notification.click()
        except NoSuchElementException as e:
            self.logger.error(e)
            try:
                turn_notification = self.driver.find_element(
                    By.XPATH, config.INSTA_NOT_NOW_BUTTON)
                turn_notification.click()
            except NoSuchElementException as e:
                self.logger.error(e)

    def get_logger(self) -> Logger:
        '''
        Get logger default log dir is `logs/insta_bot.log`
        '''
        logging.basicConfig(filename='logs/insta_bot.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        return logging.getLogger(__name__)

    def get_driver(self) -> \
            Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]:
        '''
        Get driver object and open instagram page
        '''
        selenium_driver = SeleniumDriver()
        selenium_driver.add_options("start-maximized")
        driver = selenium_driver.setup().get_driver()
        driver.get(config.INSTA_URL)
        sleep(10)
        return driver
