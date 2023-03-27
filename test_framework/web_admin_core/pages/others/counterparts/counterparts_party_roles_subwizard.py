from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsPartyRolesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_party_id_source_at_party_roles_tab(self, value):
        self.select_value_from_dropdown_list(CounterpartsConstants.PARTY_ID_SOURCE_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_venue_counterpart_id_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.VENUE_COUNTERPART_ID_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_party_role_at_party_roles_tab(self, value):
        self.select_value_from_dropdown_list(CounterpartsConstants.PARTY_ROLE_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_ext_id_client_at_party_roles_tab(self, value):
        self.set_text_by_xpath(CounterpartsConstants.EXT_ID_CLIENT_AT_PARTY_ROLES_TAB_XPATH, value)

    def set_party_role_qualifier_at_party_roles_tab(self, value):
        self.select_value_from_dropdown_list(CounterpartsConstants.PARTY_ROLE_QUALIFIER_AT_PARTY_ROLES_TAB_XPATH, value)

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

    def set_required_fields_in_party_role_tab(self, party_id_source, venue_counterpart_id, party_role, ext_id_client):
        self.set_party_id_source_at_party_roles_tab(party_id_source)
        self.set_venue_counterpart_id_at_party_roles_tab(venue_counterpart_id)
        self.set_party_role_at_party_roles_tab(party_role)
        self.set_ext_id_client_at_party_roles_tab(ext_id_client)

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

    def get_number_of_items_at_party_roles_tab(self):
        return self.find_elements_by_xpath(CounterpartsConstants.ITEMS_INTO_PARTY_ROLES_TAB_XPATH)
