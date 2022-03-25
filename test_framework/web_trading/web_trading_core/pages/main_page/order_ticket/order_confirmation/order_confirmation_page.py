from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.order_ticket.order_confirmation.order_confirmation_constants import OrderConfirmationConstants


class OrderConfirmationPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)


    def get_client_id(self):
        return self.find_by_xpath(OrderConfirmationConstants.CLIENT_ID_XPATH).text


    def get_cash_account_id(self):
        return self.find_by_xpath(OrderConfirmationConstants.CASH_ACCOUNT_ID_XPATH).text


    def get_security_account_id(self):
        return self.find_by_xpath(OrderConfirmationConstants.SECURITY_ACCOUNT_ID_XPATH).text


    def get_listing(self):
        return self.find_by_xpath(OrderConfirmationConstants.LISTING_XPATH).text


    def get_security_id(self):
        return self.find_by_xpath(OrderConfirmationConstants.SECURITY_ID_XPATH).text


    def get_side(self):
        return self.find_by_xpath(OrderConfirmationConstants.SIDE_XPATH).text


    def get_quantity(self):
        return self.find_by_xpath(OrderConfirmationConstants.QUANTITY_XPATH).text


    def get_limit_price(self):
        return self.find_by_xpath(OrderConfirmationConstants.LIMIT_PRICE_XPATH).text


    def get_order_validity(self):
        return self.find_by_xpath(OrderConfirmationConstants.ORDER_VALIDITY_XPATH).text


    def get_good_till_date(self):
        return self.find_by_xpath(OrderConfirmationConstants.GOOD_TILL_DATE_XPATH).text


    def get_venue(self):
        return self.find_by_xpath(OrderConfirmationConstants.VENUE_XPATH).text


    def get_available_cash(self):
        return self.find_by_xpath(OrderConfirmationConstants.AVAILABLE_CASH_XPATH).text


    def get_fx_rate_applied(self):
        return self.find_by_xpath(OrderConfirmationConstants.FX_RATE_APPLIED_XPATH).text


    def get_order_value(self):
        return self.find_by_xpath(OrderConfirmationConstants.ORDER_VALUE_XPATH).text


    def get_comission(self):
        return self.find_by_xpath(OrderConfirmationConstants.COMISSION_XPATH).text


    def get_total_value(self):
        return self.find_by_xpath(OrderConfirmationConstants.TOTAL_VALUE_XPATH).text


    def get_cash_balance(self):
        return self.find_by_xpath(OrderConfirmationConstants.CASH_BALANCE_XPATH).text

    def click_on_place_button(self):
        self.find_by_xpath(OrderConfirmationConstants.PLACE_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(OrderConfirmationConstants.CANCEL_BUTTON_XPATH).click()
