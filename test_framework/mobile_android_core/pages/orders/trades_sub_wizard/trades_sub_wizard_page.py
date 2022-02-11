from test_framework.mobile_android_core.pages.orders.trades_sub_wizard.trades_sub_wizard_constants import \
    TradesSubWizardConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class TradesSubWizardPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    def click_on_trades_side(self):
        self.find_by_xpath(TradesSubWizardConstants.TRADES_SIDE).click()

    def get_order_information(self):
        pass

    def swipe_right_for_re_order(self):
        pass

