import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.others.user_instr_symb_black_out.user_instr_symb_black_out_constants import \
    UserInstrSymbBlackOutConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UserInstrSymbBlackOutPeriodsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_DELETE_BUTTON_XPATH).click()

    def set_black_out_period(self, value):
        self.set_text_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_BLACK_OUT_PERIOD_XPATH, value)

    def get_black_out_period(self):
        return self.get_text_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_BLACK_OUT_PERIOD_XPATH)

    def set_black_out_period_filter(self, value):
        self.set_text_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_BLACK_OUT_PERIOD_FILTER_XPATH, value)

    def set_upper_qty(self, value):
        self.set_text_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_UPPER_QTY_XPATH, value)

    def get_upper_qty(self):
        return self.get_text_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_UPPER_QTY_XPATH)

    def set_upper_qty_filer(self, value):
        self.set_text_by_xpath(UserInstrSymbBlackOutConstants.PERIODS_TAB_UPPER_QTY_FILTER_XPATH, value)
