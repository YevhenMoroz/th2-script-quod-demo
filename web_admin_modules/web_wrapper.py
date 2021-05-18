""" This module contains functions which are used in web test cases """

import logging

from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Event, EventBatch, EventID
from uuid import uuid1
from stubs import Stubs

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.common.exceptions import NoSuchElementException

from google.protobuf.timestamp_pb2 import Timestamp
from typing import Callable, Any


def get_report(name: str, status: int, parent_id: EventID, timestamp: Timestamp):
    """ Creates TH2 event
        Parameters:
            name (str): the name of event;
            status (int): the status of event (0 - passed, 1 - failed);
            parent_id (EventID): ID of the parent event;
            timestamp (Timestamp): finish timestamp.
        Returns:
            TH2 event """
    estore = Stubs.factory.event_batch_router
    event = Event(
        id=EventID(id=str(uuid1())),
        name=name,
        status=status,
        body=b'',
        start_timestamp=timestamp,
        end_timestamp=bca.get_timestamp(),
        parent_id=parent_id)
    estore.send(EventBatch(events=[event]))


def call(method: Callable, case_id: EventID, *args: Any):
    """ Executes method and create report depends on this method
        Parameters:
            method (Callable): function for execute;
            case_id (EventID): ID of the root event;
            *args (Any): arguments for function (drivers for login, logout, etc.).
        Returns:
            TH2 report """
    method_name = method.__name__
    logging.info(f'Executing [{method_name}] method ... ')
    start_timestamp = bca.get_timestamp()
    report_status = 0
    try:
        method(*args)
    except Exception:
        report_status = 1
        logging.error(f'Error execution [{method_name}] method', exc_info=True)
    finally:
        get_report(method_name, report_status, case_id, start_timestamp)
        logging.info('done\n')


def login(web_driver: WebDriver, wait_driver: WebDriverWait):
    """ Login method
        Parameters:
            web_driver (WebDriver): browser web-driver;
            wait_driver (WebDriverWait): wait-driver for web-driver.
        Returns:
            Login action """
    web_driver.get(Stubs.custom_config['web_admin_url'])
    login_input = wait_driver.until(EC.presence_of_element_located((By.NAME, 'userID')))
    password_input = wait_driver.until(EC.presence_of_element_located((By.NAME, 'password')))
    login_input.click()
    login_input.send_keys(Stubs.custom_config['web_admin_login'])
    password_input.click()
    password_input.send_keys(Stubs.custom_config['web_admin_password'], Keys.ENTER)
    wait_driver.until(EC.presence_of_element_located((By.ID, 'app-sidenav-menu')))


def logout(wait_driver: WebDriverWait):
    """ Logout method
        Parameters:
            wait_driver (WebDriverWait): wait-driver for web-driver.
        Returns:
            Logout action """
    logout_btn = wait_driver.until(EC.presence_of_element_located((By.XPATH, '//mat-toolbar/button')))
    logout_btn.click()
    confirm_btn = wait_driver.until(EC.presence_of_element_located((By.XPATH,
                                                                    '//*[text()="OK"]')))
    confirm_btn.click()
    wait_driver.until(EC.presence_of_element_located((By.ID, 'login')))


def check_exists_by_xpath(web_driver: WebDriver, xpath: str) -> bool:
    """ Returns True if element exists or False if is not
        Parameters:
            web_driver (WebDriver): browser web-driver;
            xpath (str): xpath for element.
        Returns:
            Bool """
    try:
        web_driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def check_is_clickable(web_element: WebElement) -> bool:
    """ Returns True if element clickable
        Parameters:
            web_element (WebElement): web element.
        Returns:
            Bool """
    return web_element.is_displayed() and web_element.is_enabled()
