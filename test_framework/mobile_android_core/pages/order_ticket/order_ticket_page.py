from test_framework.mobile_android_core.pages.order_ticket.order_ticket_constants import OrderTicketConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class OrderTicketPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    def click_back_button(self):
        self.find_by_xpath(OrderTicketConstants.ARROW_BACK).click()

    def click_on_buy_side(self):
        self.find_by_xpath(OrderTicketConstants.BUY_SIDE).click()

    def click_on_sell_side(self):
        self.find_by_xpath(OrderTicketConstants.SELL_SIDE).click()

    def click_on_instrument(self, instrument):
        pass

    def set_account(self, account):
        pass

    def get_account(self):
        pass

    def set_quantity(self, quantity):
        pass

    def get_quantity(self):
        pass

    def set_price(self, price):
        pass

    def get_price(self):
        pass

    def set_order_type(self, order_type):
        pass

    def get_order_type(self):
        pass

    def set_time_in_force(self, time_in_force):
        pass

    def get_time_in_force(self):
        pass

    # region expire date
    def click_on_expire_date(self):
        pass

    def click_on_edit_at_expire_date(self):
        pass

    def click_on_cancel_at_expire_date(self):
        pass

    def click_on_ok_at_expire_date(self):
        pass
    # endregion
