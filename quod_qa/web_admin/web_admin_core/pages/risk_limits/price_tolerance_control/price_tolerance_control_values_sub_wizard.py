from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.price_tolerance_control.price_tolerance_control_constants import \
    PriceToleranceControlConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class PriceToleranceControlSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self,value):
        self.set_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_NAME_XPATH,value)

    def get_name(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_NAME_XPATH)

    def set_external_id(self,value):
        self.set_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_EXTERNAL_ID_XPATH,value)

    def get_external_id(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_EXTERNAL_ID_XPATH)

    def set_listing_group(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_LISTING_GROUP_XPATH,value)

    def get_listing_group(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_LISTING_GROUP_XPATH)

    def set_instr_type(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_INSTR_TYPE_XPATH,value)

    def get_instr_type(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_INSTR_TYPE_XPATH)

    def set_listing(self, value):
        self.set_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_LISTING_XPATH,value)

    def get_listing(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_LISTING_XPATH)

    def click_on_wildcard_listing_checkbox(self):
        self.find_by_xpath(PriceToleranceControlConstants.VALUES_TAB_WILDCARD_LISTING_CHECKBOX_XPATH).click()

    def set_user(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_USER_XPATH,value)

    def get_user(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_USER_XPATH)

    def set_client(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_CLIENT_XPATH,value)

    def get_client(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_CLIENT_XPATH)

    def set_client_group(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_CLIENT_GROUP_XPATH,value)

    def get_client_group(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_CLIENT_GROUP_XPATH)

    def set_venue(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_VENUE_XPATH,value)

    def get_venue(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_VENUE_XPATH)

    def set_sub_venue(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.VALUES_TAB_SUB_VENUE_XPATH,value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.VALUES_TAB_SUB_VENUE_XPATH)











































