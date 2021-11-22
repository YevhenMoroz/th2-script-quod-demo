""" This module contains functions which are used in web test cases """

import logging
import time

from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Event, EventBatch, EventID
from uuid import uuid1

from custom.verifier import Verifier
from stubs import Stubs

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.common.exceptions import NoSuchElementException

from google.protobuf.timestamp_pb2 import Timestamp
from typing import Callable, Any

import ExactPro_examples.web_admin_modules.locator_xpath as get_xpath


def get_report(name: str, status: int, parent_id: EventID, timestamp: Timestamp) -> None:
    """ Creates TH2 event
        Parameters:
            name (str): the name of event;
            status (int): the status of event (0 - passed, 1 - failed);
            parent_id (EventID): ID of the parent event;
            timestamp (Timestamp): finish timestamp.
        Returns:
            None """
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


def call(method: Callable, case_id: EventID, event_name: str, *args: Any) -> Any:
    """ Executes method and create report depends on this method
        Parameters:
            method (Callable): function for execute;
            case_id (EventID): ID of the root event;
            event_name(str): event name for TH2 report
            *args (Any): arguments for function (drivers for login, logout, etc.).
        Returns:
            Any """
    method_name = method.__name__
    logging.info(f'Executing [{method_name}] method ... ')
    start_timestamp = bca.get_timestamp()
    report_status = 0
    try:
        return method(*args)
    except Exception:
        report_status = 1
        logging.error(f'Error execution [{method_name}] method', exc_info=True)
    finally:
        get_report(event_name, report_status, case_id, start_timestamp)
        logging.info('done\n')


def login(web_driver: WebDriver, wait_driver: WebDriverWait, environment: str) -> None:
    """ Login method
        Parameters:
            web_driver (WebDriver): browser driver;
            wait_driver (WebDriverWait): wait driver for browser driver;
            environment (str): web environment (303/305)
        Returns:
            None """
    web_driver.get(Stubs.custom_config[f'web_admin_url_{environment}'])
    login_input = wait_driver.until(EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text('User Name'))))
    password_input = wait_driver.until(EC.presence_of_element_located((By.XPATH, get_xpath.input_by_text('Password'))))
    login_input.send_keys(Stubs.custom_config['web_admin_login'])
    password_input.send_keys(Stubs.custom_config['web_admin_password'], Keys.ENTER)
    wait_driver.until(EC.presence_of_element_located((By.XPATH, get_xpath.sidebar_menu_tab_by_title('General'))))


def logout(wait_driver: WebDriverWait) -> None:
    """ Logout method
        Parameters:
            wait_driver (WebDriverWait): wait-driver for web-driver.
        Returns:
            None """
    person_btn = wait_driver.until(EC.presence_of_element_located((By.XPATH, get_xpath.person_btn)))
    person_btn.click()
    logout_btn = wait_driver.until(EC.presence_of_element_located((By.XPATH, get_xpath.logout_btn)))
    logout_btn.click()
    wait_driver.until(EC.presence_of_element_located((By.XPATH, get_xpath.login_logo)))


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


def verify_row_count(case_id: EventID, event_name: str, expected_count: int, actual_count: int) -> None:
    """ Verify row count and returns TH2-verify event
        Parameters:
            case_id (EventID): ID of the root event;
            event_name (str): name of verify event;
            expected_count (int): expected result row count;
            actual_count (int): actual result row count.
        Returns:
            None """
    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    verifier.compare_values('Count', str(expected_count), str(actual_count))
    verifier.verify()


def filter_grid_by_field(web_driver: WebDriver, filter_name: str, query: str) -> int:
    """ Filters data in table by filter name and waits until data refresh in table, returns data count
        Parameters:
            web_driver (WebDriver): browser web-driver;
            filter_name (WebElement): name of filter field;
            query (str): query.
        Returns:
            int """
    filter_list = web_driver.find_elements_by_xpath(get_xpath.table_filter_names)
    desired_filter = web_driver.find_element_by_xpath(get_xpath.table_filter_name_by_text(filter_name))
    desired_filter_index = filter_list.index(desired_filter)
    filter_input = web_driver.find_element_by_xpath(get_xpath.table_filter_inputs +
                                                    f'[{desired_filter_index + 1}]' +
                                                    f'{get_xpath.filter_input}')
    row_container = web_driver.find_element_by_xpath(get_xpath.table_row_container)
    row_xpath = get_xpath.table_row
    row_count = len(row_container.find_elements_by_xpath(row_xpath))
    result_row_count = row_count
    filter_input.clear()
    filter_input.send_keys(query)
    timeout = time.time() + 5
    while result_row_count == row_count and time.time() <= timeout:
        result_row_count = len(row_container.find_elements_by_xpath(row_xpath))
    return result_row_count
