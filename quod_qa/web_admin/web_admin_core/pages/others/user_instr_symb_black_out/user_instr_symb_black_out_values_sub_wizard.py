import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.user_instr_symb_black_out.user_instr_symb_black_out_constants import \
    UserInstrSymbBlackOutConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UserInstrSymbBlackOutValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_symbol(self, value):
        self.set_combobox_value(UserInstrSymbBlackOutConstants.VALUES_TAB_SYMBOL_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(UserInstrSymbBlackOutConstants.VALUES_TAB_SYMBOL_XPATH)

    def set_user(self, value):
        self.set_combobox_value(UserInstrSymbBlackOutConstants.VALUES_TAB_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(UserInstrSymbBlackOutConstants.VALUES_TAB_USER_XPATH)
