import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name_value_at_values_tab(self, new_name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_AT_VALUES_TAB_XPATH, new_name)

    def get_name_at_values_tab(self):
        return self.get_text_by_xpath(CounterpartsConstants.NAME_AT_VALUES_TAB_XPATH)

    def click_on_plus_sub_counterparts(self):
        self.find_by_xpath(CounterpartsConstants.PLUS_AT_SUB_COUNTERPARTS_TAB_XPATH).click()

    def click_on_plus_party_roles(self):
        self.find_by_xpath(CounterpartsConstants.PLUS_BUTTON_AT_PARTY_ROLES_TAB_XPATH).click()

    def click_on_pdf_button(self):
        self.find_by_xpath(CounterpartsConstants.DOWNLOAD_PDF_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value: str):
        self.clear_download_directory()
        self.find_by_xpath(CounterpartsConstants.DOWNLOAD_PDF_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_check_mark(self):
        self.find_by_xpath(CounterpartsConstants.CHECK_MARK_XPATH).click()

    def click_on_close_changes(self):
        self.find_by_xpath(CounterpartsConstants.CLOSE_CHANGES_AT_COUNTERPARTS_TABS_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(CounterpartsConstants.CLOSE_COUNTERPARTS_WIZARD_XPATH).click()

    def click_on_edit_at_sub_counterparts_tab(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_SUB_COUNTERPARTS_TAB_XPATH).click()

    def click_on_edit_at_party_roles_tab(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_PARTY_ROLES_TAB_XPATH).click()

    def click_on_delete_at_sub_counterparts_tab(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_COUNTERPARTS_TABS_XPATH).click()

    def click_on_delete_at_party_roles_tab(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_PARTY_ROLES_TABS_XPATH).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(CounterpartsConstants.CLEAR_CHANGES_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(CounterpartsConstants.REVERT_CHANGES_AT_COUNTERPARTS_TAB_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(CounterpartsConstants.SAVE_CHANGES_XPATH).click()

    # ----sub counterparts---
    def set_name_at_sub_counterparts_tab(self, name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_AT_SUB_COUNTERPARTS_TAB_XPATH, name)

    def set_party_id_at_sub_counterparts_tab(self, party_id):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ID_AT_SUB_COUNTERPARTS_TAB_XPATH, party_id)

    def set_ext_id_client_at_sub_counterparts_tab(self, ext_id_client):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_AT_SUB_COUNTERPARTS_TAB_XPATH, ext_id_client)

    def set_party_sub_id_at_sub_counterparts_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_SUB_ID_TYPE_AT_SUB_COUNTERPARTS_TAB_XPATH, value)

    # --sub counterparts filters--
    def set_name_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.NAME_FILTER_AT_SUB_COUNTERPARTS_TAB_XPATH, value)

    def set_party_id_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ID_FILTER_AT_SUB_COUNTERPARTS_TAB_XPATH, value)

    def set_ext_id_client_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_FILTER_AT_SUB_COUNTERPARTS_TAB_XPATH, value)

    def set_party_sub_id_type_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_SUB_ID_TYPE_FILTER_AT_SUB_TYPE_XPATH, value)

    # --getters--
    def get_name_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.NAME_VALUE_AT_SUB_COUNTERPARTS_TAB_XPATH).text

    def get_party_id_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ID_VALUE_AT_SUB_COUNTERPARTS_TAB_XPATH).text

    def get_ext_id_client_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.EXT_ID_VALUE_CLIENT_AT_SUB_COUNTERPARTS_TAB_XPATH).text

    def get_party_sub_id_type_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_SUB_ID_VALUE_TYPE_AT_SUB_COUNTERPARTS_TAB_XPATH).text

    # ----Party roles----
    def set_party_id_source_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_ID_SOURCE_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_venue_counterpart_id_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_party_role_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_ROLE_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_ext_id_client_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_party_role_qualifier_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_ROLE_QUALIFIER_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_venue_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.VENUE_AT_PARTY_ROLES_TAB_XPATH, value)

    # --party role filters--
    def set_party_id_source_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ID_SOURCE_FILTER_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_venue_counterpart_id_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_FILTER_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_party_role_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ROLE_FILTER_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_ext_id_client_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_FILTER_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_party_role_qualifier_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ROLE_QUALIFIER_FILTER_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_venue_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_FILTER_AT_PARTY_ROLES_TAB_XPATH, value)

    # --getters--
    def get_party_id_source_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ID_SOURCE_VALUE_AT_PARTY_ROLES_TAB_XPATH).text

    def get_venue_counterpart_id_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_VALUE_AT_PARTY_ROLES_TAB_XPATH).text

    def get_party_role_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ROLE_VALUE_AT_PARTY_ROLES_TAB_XPATH).text

    def get_ext_id_client_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_VALUE_AT_PARTY_ROLES_TAB_XPATH).text

    def get_party_role_qualifier_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ROLE_QUALIFIER_VALUE_AT_PARTY_ROLES_TAB_XPATH).text

    def get_venue_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.VENUE_VALUE_AT_PARTY_ROLES_TAB_XPATH).text
