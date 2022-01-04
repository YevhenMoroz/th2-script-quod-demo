import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.general.mdentitlements.mdentitlements_constants import \
    MDEntitlementsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class MDEntitlementsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_user(self, value):
        self.set_combobox_value(MDEntitlementsConstants.DIMENSIONS_TAB_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(MDEntitlementsConstants.DIMENSIONS_TAB_USER_XPATH)

    def set_desk(self, value):
        self.set_combobox_value(MDEntitlementsConstants.DIMENSIONS_TAB_DESK_XPATH, value)

    def get_desk(self):
        return self.get_text_by_xpath(MDEntitlementsConstants.DIMENSIONS_TAB_DESK_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(MDEntitlementsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(MDEntitlementsConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(MDEntitlementsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(MDEntitlementsConstants.MDENTITLEMENTS_PAGE_TITLE_XPATH)

    def set_location(self, value):
        self.set_combobox_value(MDEntitlementsConstants.DIMENSIONS_TAB_LOCATION_XPATH, value)

    def get_location(self):
        return self.get_text_by_xpath(MDEntitlementsConstants.DIMENSIONS_TAB_LOCATION_XPATH)

    def clear_location_field(self):
        self.set_text_by_xpath(MDEntitlementsConstants.DIMENSIONS_TAB_LOCATION_XPATH,"")