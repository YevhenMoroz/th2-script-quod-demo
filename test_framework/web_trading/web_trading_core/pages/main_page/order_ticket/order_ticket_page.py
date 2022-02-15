import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_ticket_constants import OrderTicketConstants


class OrderTicketPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)


    def set_symbol(self, symbol):
        self.set_text_by_xpath(OrderTicketConstants.SEARCH_SYMBOL_FIELD_XPATH, symbol)
        # time.sleep(2)
        # self.find_by_xpath(OrderTicketConstants.SEARCH_SYMBOL_FIELD_XPATH).click()
        time.sleep(2)
        self.set_text_by_xpath(OrderTicketConstants.SEARCH_SYMBOL_FIELD_XPATH, symbol)
        time.sleep(4)
        self.find_by_xpath(OrderTicketConstants.LIST_OF_SYMBOL_XPATH.format(symbol)).click()
        # self.select_value_from_dropdown_list()

    def set_account(self, account):
        self.find_by_xpath(OrderTicketConstants.ACCOUNTS_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderTicketConstants.LIST_OF_ACCOUNTS_XPATH.format(account))

    def click_on_buy_mode_button(self):
        self.find_by_xpath(OrderTicketConstants.MODE_BUY_BUTTON_XPATH).click()

    def click_on_sell_mode_button(self):
        self.find_by_xpath(OrderTicketConstants.MODE_SELL_BUTTON_XPATH).click()

    def set_quantity(self, quantity):
        self.set_text_by_xpath(OrderTicketConstants.QUANTITY_FIELD_XPATH, quantity)

    def set_price(self, price):
        self.set_text_by_xpath(OrderTicketConstants.PRICE_FIELD_XPATH, price)

    def set_order_type(self, order_type):
        self.find_by_xpath(OrderTicketConstants.ORDER_TYPE_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderTicketConstants.LIST_OF_ORDER_TYPE_XPATH.format(order_type))

    def set_time_in_force(self, time_in_force):
        self.find_by_xpath(OrderTicketConstants.TIME_IN_FORCE_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderTicketConstants.LIST_OF_TIME_IN_FORCE_XPATH.format(time_in_force))

    def set_expire_date(self, expire_date):
        self.set_text_by_xpath(OrderTicketConstants.EXPIRE_DATE_FIELD_XPATH, expire_date)

    def click_on_buy_button(self):
        self.find_by_xpath(OrderTicketConstants.BUY_BUTTON_XPATH).click()

    def click_on_sell_button(self):
        self.find_by_xpath(OrderTicketConstants.SELL_BUTTON_XPATH).click()

    def click_on_close_order_ticket(self):
        self.find_by_xpath(OrderTicketConstants.CLOSE_BUTTON_XPATH).click()

    def get_error_notification(self):
        return self.find_by_xpath(OrderTicketConstants.NOTIFICATION_ACCOUNT_XPATH).text

    def create_order(self, symbol, account, quantity, price, order_type):
        self.set_symbol(symbol)
        time.sleep(2)
        self.set_account(account)
        time.sleep(2)
        self.click_on_buy_mode_button()
        time.sleep(2)
        self.set_quantity(quantity)
        time.sleep(2)
        self.set_price(price)
        time.sleep(2)
        self.set_order_type(order_type)
        time.sleep(2)