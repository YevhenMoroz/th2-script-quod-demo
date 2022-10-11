from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsSubCounterpartsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

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

    def is_name_field_required(self):
        return self.is_field_required(CounterpartsConstants.NAME_AT_SUB_COUNTERPARTS_TAB_XPATH)

    def is_party_id_field_required(self):
        return self.is_field_required(CounterpartsConstants.PARTY_ID_AT_SUB_COUNTERPARTS_TAB_XPATH)

    def is_ext_id_client_field_required(self):
        return self.is_field_required(CounterpartsConstants.EXT_ID_CLIENT_AT_SUB_COUNTERPARTS_TAB_XPATH)

    def is_party_sub_id_type_field_required(self):
        return self.is_field_required(CounterpartsConstants.PARTY_SUB_ID_TYPE_AT_SUB_COUNTERPARTS_TAB_XPATH)
