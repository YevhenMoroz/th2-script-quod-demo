import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_ticket_constants import OrderTicket


class OrderTicketPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    def set_symbol(self, symbol):
        self.set_text_by_xpath(OrderTicket.SEARCH_SYMBOL_FIELD_XPATH, symbol)

    def set_account(self, account):
        self.set_text_by_xpath(OrderTicket.ACCOUNTS_FIELD_XPATH, account)

    def click_on_buy_mode_button(self):
        self.find_by_xpath(OrderTicket.MODE_BUY_BUTTON_XPATH).click()

    def click_on_sell_mode_button(self):
        self.find_by_xpath(OrderTicket.MODE_SELL_BUTTON_XPATH).click()

    def set_quantity(self, quantity):
        self.set_text_by_xpath(OrderTicket.QUANTITY_FIELD_XPATH, quantity)

    def set_price(self, price):
        self.set_text_by_xpath(OrderTicket.PRICE_FIELD_XPATH, price)

    def set_order_type(self, order_type):
        self.find_by_xpath(OrderTicket.ORDER_TYPE_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderTicket.LIST_OF_ORDER_TYPE_XPATH.format(order_type))

    def set_time_in_force(self, time_in_force):
        self.find_by_xpath(OrderTicket.TIME_IN_FORCE_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderTicket.LIST_OF_TIME_IN_FORCE_XPATH.format(time_in_force))

    def set_expire_date(self, expire_date):
        self.set_text_by_xpath(OrderTicket.EXPIRE_DATE_FIELD_XPATH, expire_date)

    def click_on_buy_button(self):
        self.find_by_xpath(OrderTicket.BUY_BUTTON_XPATH).click()

    def click_on_sell_button(self):
        self.find_by_xpath(OrderTicket.SELL_BUTTON_XPATH).click()

    def click_on_close_order_ticket(self):
        self.find_by_xpath(OrderTicket.CLOSE_BUTTON_XPATH).click()
