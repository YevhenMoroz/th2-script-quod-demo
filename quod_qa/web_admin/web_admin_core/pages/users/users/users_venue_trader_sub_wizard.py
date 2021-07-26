from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersVenueTraderSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(UsersConstants.PLUS_BUTTON_AT_VENUE_TRADER_SUB_WIZARD).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(UsersConstants.CHECKMARK_AT_VENUE_TRADER_SUB_WIZARD).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(UsersConstants.CANCEL_AT_VENUE_TRADER_SUB_WIZARD).click()

    def click_on_edit_button(self):
        self.find_by_xpath(UsersConstants.EDIT_AT_VENUE_TRADER_SUB_WIZARD).click()

    def click_on_delete_button(self):
        self.find_by_xpath(UsersConstants.DELETE_AT_VENUE_TRADER_SUB_WIZARD).click()

    def click_on_manage_trader_groups(self):
        self.find_by_xpath(UsersConstants.MANAGE_TRADER_GROUPS_AT_VENUE_TRADER_SUB_WIZARD).click()

    # get and set

    def set_venue(self,value):
        self.set_combobox_value(UsersConstants.VENUE_AT_VENUE_TRADER_SUB_WIZARD, value)

    def get_venue(self):
        return self.get_text_by_xpath(UsersConstants.VENUE_AT_VENUE_TRADER_SUB_WIZARD)

    def set_venue_trader_name(self, value):
        self.set_text_by_xpath(UsersConstants.VENUE_TRADER_NAME_AT_VENUE_TRADER_SUB_WIZARD, value)

    def get_venue_trader_name(self):
        return self.get_text_by_xpath(UsersConstants.VENUE_TRADER_NAME_AT_VENUE_TRADER_SUB_WIZARD)

    def set_trader_group(self, value):
        self.set_combobox_value(UsersConstants.TRADER_GROUP_AT_VENUE_TRADER_SUB_WIZARD, value)

    def get_trader_group(self):
        self.get_text_by_xpath(UsersConstants.TRADER_GROUP_AT_VENUE_TRADER_SUB_WIZARD)

    # filters
    def set_venue_filter(self, value):
        self.set_text_by_xpath(UsersConstants.VENUE_FILTER_AT_VENUE_TRADER_SUB_WIZARD, value)

    def set_venue_trader_name_filter(self,value):
        self.set_text_by_xpath(UsersConstants.VENUE_TRADER_NAME_AT_VENUE_TRADER_SUB_WIZARD, value)

    def set_trader_group_filter(self, value):
        self.set_text_by_xpath(UsersConstants.TRADER_GROUP_FILTER_AT_VENUE_TRADER_SUB_WIZARD, value)







