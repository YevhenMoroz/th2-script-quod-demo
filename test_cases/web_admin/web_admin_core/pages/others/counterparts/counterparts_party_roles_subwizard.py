from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsPartyRolesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

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
