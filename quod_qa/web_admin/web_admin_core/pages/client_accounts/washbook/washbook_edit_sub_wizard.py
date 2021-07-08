from quod_qa.web_admin.web_admin_core.pages.client_accounts.washbook.washbook_constants import WashBookConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookEditSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(WashBookConstants.SAVE_CHANGES_AT_EDIT_SUB_WIZARD).click()

    # region setters and getters

    def set_since_inception_pl(self, value):
        self.set_text_by_xpath(WashBookConstants.SINCE_INCEPTION_PL, value)

    def get_since_inception_pl(self):
        return self.get_text_by_xpath(WashBookConstants.SINCE_INCEPTION_PL)

    def set_month_pl(self, value):
        self.set_text_by_xpath(WashBookConstants.MONTH_PL, value)

    def get_month_pl(self):
        return self.get_text_by_xpath(WashBookConstants.MONTH_PL)

    def set_week_pl(self, value):
        self.set_text_by_xpath(WashBookConstants.WEEK_PL, value)

    def get_week_pl(self):
        return self.get_text_by_xpath(WashBookConstants.WEEK_PL)

    def set_quarter_pl(self, value):
        self.set_text_by_xpath(WashBookConstants.QUARTER_PL, value)

    def get_quarter_pl(self):
        return self.get_text_by_xpath(WashBookConstants.QUARTER_PL)

    def set_year_pl(self, value):
        self.set_text_by_xpath(WashBookConstants.YEAR_PL, value)

    def get_year_pl(self):
        return self.get_text_by_xpath(WashBookConstants.YEAR_PL)
    # endregion
