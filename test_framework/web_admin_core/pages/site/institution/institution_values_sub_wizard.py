import time
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstitutionsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_institution_name(self, value):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_INSTITUTION_NAME, value)

    def get_institution_name(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_INSTITUTION_NAME)

    def is_tab_collapsed(self):
        return True if "true" in self.find_by_xpath(InstitutionsConstants.VALUES_TAB).get_attribute("aria-expanded") else False

    def set_lei(self, value):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_LEI_NAME, value)

    def get_lei(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_LEI_NAME)

    def set_ctm_bic(self, value):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_CTM_BIC_NAME, value)

    def get_ctm_bic(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_CTM_BIC_NAME)

    def set_counterpart(self, value):
        self.set_combobox_value(InstitutionsConstants.VALUES_TAB_COUNTERPART_NAME, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_COUNTERPART_NAME)

    def click_on_manage_counterpart(self):
        self.find_by_xpath(InstitutionsConstants.VALUES_TAB_MANAGE_COUNTERPART_BUTTON_XPATH).click()

    def set_client_time_zone(self, value):
        self.set_combobox_value(InstitutionsConstants.VALUES_TAB_CLIENT_TIME_ZONE_XPATH, value)

    def get_client_time_zone(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_CLIENT_TIME_ZONE_XPATH)

    def get_all_client_time_zone_from_drop_menu(self):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_CLIENT_TIME_ZONE_XPATH, "")
        time.sleep(1)
        return self._get_all_items_from_drop_down(InstitutionsConstants.DROP_DOWN_MENU_XPATH)

    def set_position_flattening_period(self, value):
        """
        value must be of type xx:xx
        """
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD, value)

    def get_position_flattening_period(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_POSITION_FLATTENING_PERIOD)

    def click_at_select_unknown_accounts_checkbox(self):
        self.find_by_xpath(InstitutionsConstants.VALUES_TAB_UNKNOWN_ACCOUNTS).click()

    def is_select_unknown_accounts_selected(self):
        return self.is_checkbox_selected(InstitutionsConstants.VALUES_TAB_UNKNOWN_ACCOUNTS)
