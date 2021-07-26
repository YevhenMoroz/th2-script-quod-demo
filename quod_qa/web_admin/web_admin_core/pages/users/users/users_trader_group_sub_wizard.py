from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersTraderGroupSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(UsersConstants.PLUS_BUTTON_AT_TRADER_GROUPS_SUB_WIZARD).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(UsersConstants.CHECKMARK_AT_TRADER_GROUPS_SUB_WIZARD).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(UsersConstants.CANCEL_AT_TRADER_GROUPS_SUB_WIZARD).click()

    def click_on_go_back(self):
        self.find_by_xpath(UsersConstants.GO_BACK_BUTTON)
    # get and set

    def set_name(self, value):
        self.set_text_by_xpath(UsersConstants.NAME_AT_TRADER_GROUPS_SUB_WIZARD, value)

    def get_name(self):
        return self.get_text_by_xpath(UsersConstants.NAME_AT_TRADER_GROUPS_SUB_WIZARD)

    def set_venue_trader_group_id(self, value):
        self.set_text_by_xpath(UsersConstants.VENUE_TRADER_GROUP_ID_AT_TRADER_GROUPS, value)

    def get_venue_trader_group_id(self):
        return self.get_text_by_xpath(UsersConstants.VENUE_TRADER_GROUP_ID_AT_TRADER_GROUPS)

    # filter
    def set_name_filter(self, value):
        self.set_text_by_xpath(UsersConstants.NAME_FILTER_AT_TRADER_GROUPS_SUB_WIZARD, value)

    def set_venue_trader_group_id_filter(self, value):
        self.set_text_by_xpath(UsersConstants.VENUE_TRADER_GROUP_ID_FILTER_AT_TRADER_GROUPS_SUB_WIZARD, value)
