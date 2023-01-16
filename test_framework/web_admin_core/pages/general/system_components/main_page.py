from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.system_components.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.EDIT_BUTTON).click()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.MoreActions.PIN_BUTTON).click()

    def set_instance_id(self, value):
        self.set_text_by_xpath(Constants.MainPage.INSTANCE_ID_FILTER, value)

    def set_short_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.SHORT_NAME_FILTER, value)

    def set_long_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.LONG_NAME_FILTER, value)

    def set_version(self, value):
        self.set_text_by_xpath(Constants.MainPage.VERSION_FILTER, value)

    def set_active(self, value):
        self.set_text_by_xpath(Constants.MainPage.ACTIVE_FILTER, value)

    def is_searched_entity_found_by_name(self, name):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(name))

    def is_entity_pinned(self, name):
        return self.is_element_present(Constants.MainPage.PINNED_ENTITY.format(name))

    def is_active_status_displayed(self):
        return self.is_element_present(Constants.MainPage.ACTIVE_STATUS_ICON)
