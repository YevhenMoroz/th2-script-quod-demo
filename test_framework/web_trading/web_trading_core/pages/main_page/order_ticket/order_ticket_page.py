from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderTicketPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    def set_symbol(self, symbol: str):
        pass

    def set_account(self, account: str):
        pass

    def click_on_buy_mode_button(self):
        pass

    def click_on_sell_mode_button(self):
        pass

    def set_quantity(self, quantity):
        pass

    def set_price(self, price):
        pass

    def set_order_type(self, order_type):
        pass

    def set_time_in_force(self, time_in_force):
        pass

    def set_expire_date(self, expire_date):
        pass

    def click_on_buy_button(self):
        pass

    def click_on_sell_button(self):
        pass

    def click_on_close_order_ticket(self):
        pass
