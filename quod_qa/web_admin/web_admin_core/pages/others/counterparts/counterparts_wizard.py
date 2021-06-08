from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name_value_at_values_tab(self, new_name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_AT_VALUES_TAB, new_name)

    def get_name_at_values_tab(self):
        return self.get_text_by_xpath(CounterpartsConstants.NAME_AT_VALUES_TAB)

    def click_on_plus_sub_counterparts(self):
        self.find_by_xpath(CounterpartsConstants.PLUS_AT_SUB_COUNTERPARTS_TAB).click()

    def click_on_plus_party_roles(self):
        self.find_by_xpath(CounterpartsConstants.PLUS_BUTTON_AT_PARTY_ROLES_TAB).click()

    def click_on_check_mark(self):
        self.find_by_xpath(CounterpartsConstants.CHECK_MARK).click()

    def click_on_close_changes(self):
        self.find_by_xpath(CounterpartsConstants.CLOSE_CHANGES_AT_COUNTERPARTS_TABS).click()

    def click_on_close(self):
        self.find_by_xpath(CounterpartsConstants.CLOSE_COUNTERPARTS_WIZARD).click()

    def click_on_edit(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_COUNTERPARTS_TABS).click()

    def click_on_delete(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_COUNTERPARTS_TABS).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(CounterpartsConstants.CLEAR_CHANGES).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(CounterpartsConstants.REVERT_CHANGES_AT_COUNTERPARTS_TAB).click()

    def click_on_save_changes(self):
        self.find_by_xpath(CounterpartsConstants.SAVE_CHANGES).click()

    # ----sub counterparts---
    def set_name_at_sub_counterparts_tab(self, name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_AT_SUB_COUNTERPARTS_TAB, name)

    def set_party_id_at_sub_counterparts_tab(self, party_id):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ID_AT_SUB_COUNTERPARTS_TAB, party_id)

    def set_ext_id_client_at_sub_counterparts_tab(self, ext_id_client):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_AT_SUB_COUNTERPARTS_TAB, ext_id_client)

    def set_party_sub_id_at_sub_counterparts_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_SUB_ID_TYPE_AT_SUB_COUNTERPARTS_TAB, value)

    # --sub counterparts filters--
    def set_name_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.NAME_FILTER_AT_SUB_COUNTERPARTS_TAB, value)

    def set_party_id_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ID_FILTER_AT_SUB_COUNTERPARTS_TAB, value)

    def set_ext_id_client_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_FILTER_AT_SUB_COUNTERPARTS_TAB, value)

    def set_party_sub_id_type_filter_at_sub_counterparts_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_SUB_ID_TYPE_FILTER_AT_SUB_TYPE, value)

    # --getters--
    def get_name_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.NAME_VALUE_AT_SUB_COUNTERPARTS_TAB).text

    def get_party_id_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ID_VALUE_AT_SUB_COUNTERPARTS_TAB).text

    def get_ext_id_client_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.EXT_ID_VALUE_CLIENT_AT_SUB_COUNTERPARTS_TAB).text

    def get_party_sub_id_type_value_at_sub_counterparts_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_SUB_ID_VALUE_TYPE_AT_SUB_COUNTERPARTS_TAB).text

    # ----Party roles----
    def set_party_id_source_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_ID_SOURCE_AT_PARTY_ROLES_TAB, value)

    def set_venue_counterpart_id_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_AT_PARTY_ROLES_TAB, value)

    def set_party_role_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_ROLE_AT_PARTY_ROLES_TAB, value)

    def set_ext_id_client_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_AT_PARTY_ROLES_TAB, value)

    def set_party_role_qualifier_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.PARTY_ROLE_QUALIFIER_AT_PARTY_ROLES_TAB, value)

    def set_venue_at_party_roles_tab(self, value):
        self.set_combobox_value(CounterpartsConstants.VENUE_AT_PARTY_ROLES_TAB, value)

    # --party role filters--
    def set_party_id_source_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ID_SOURCE_FILTER_AT_PARTY_ROLES_TAB, value)

    def set_venue_counterpart_id_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_FILTER_AT_PARTY_ROLES_TAB, value)

    def set_party_role_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ROLE_FILTER_AT_PARTY_ROLES_TAB, value)

    def set_ext_id_client_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_FILTER_AT_PARTY_ROLES_TAB, value)

    def set_party_role_qualifier_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.PARTY_ROLE_QUALIFIER_FILTER_AT_PARTY_ROLES_TAB, value)

    def set_venue_filter_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_FILTER_AT_PARTY_ROLES_TAB, value)

    # --getters--
    def get_party_id_source_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ID_SOURCE_VALUE_AT_PARTY_ROLES_TAB).text

    def get_venue_counterpart_id_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_VALUE_AT_PARTY_ROLES_TAB).text

    def get_party_role_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ROLE_VALUE_AT_PARTY_ROLES_TAB).text

    def get_ext_id_client_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_VALUE_AT_PARTY_ROLES_TAB).text

    def get_party_role_qualifier_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.PARTY_ROLE_QUALIFIER_VALUE_AT_PARTY_ROLES_TAB).text

    def get_venue_value_at_party_roles_tab(self):
        return self.find_by_xpath(CounterpartsConstants.VENUE_VALUE_AT_PARTY_ROLES_TAB).text
