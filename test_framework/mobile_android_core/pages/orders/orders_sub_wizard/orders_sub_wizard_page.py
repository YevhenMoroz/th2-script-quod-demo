from test_framework.mobile_android_core.pages.orders.orders_sub_wizard.orders_sub_wizard_constants import \
    OrdersSubWizardConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class OrdersSubWizardPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    def click_on_orders_side(self):
        self.find_by_xpath(OrdersSubWizardConstants.ORDERS_SIDE).click()

    def get_order_information(self):
        pass

    def swipe_right_for_re_order(self):
        pass

