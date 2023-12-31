import time


from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.others.user_instr_symb_black_out.user_instr_symb_black_out_constants import \
    UserInstrSymbBlackOutConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UserInstrSymbBlackOutWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close_wizard(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(UserInstrSymbBlackOutConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(UserInstrSymbBlackOutConstants.GO_BACK_BUTTON_XPATH).click()

