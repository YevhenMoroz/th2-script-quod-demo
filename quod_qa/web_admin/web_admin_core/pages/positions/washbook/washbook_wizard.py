from quod_qa.web_admin.web_admin_core.pages.positions.washbook.washbook_constants import WashBookConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region ~~VALUES TAB~~ get. and set.

    def set_id_at_values_tab(self, value):
        self.set_text_by_xpath(WashBookConstants.ID_AT_VALUES_TAB, value)

    def get_id_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.ID_AT_VALUES_TAB)

    def set_ext_id_client_at_values_tab(self, value):
        self.set_text_by_xpath(WashBookConstants.EXT_ID_CLIENT_AT_VALUES_TAB, value)

    def get_ext_id_client_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.EXT_ID_CLIENT_AT_VALUES_TAB)

    def set_client_at_values_tab(self, value):
        self.set_combobox_value(WashBookConstants.CLIENT_AT_VALUES_TAB, value)

    def get_client_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.CLIENT_AT_VALUES_TAB)

    def set_description_at_values_tab(self, value):
        self.set_text_by_xpath(WashBookConstants.DESCRIPTION_AT_VALUES_TAB, value)

    def get_description_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.DESCRIPTION_AT_VALUES_TAB)

    def set_clearing_account_type_at_values_tab(self, value):
        self.set_combobox_value(WashBookConstants.CLEARING_ACCOUNT_TYPE_AT_VALUES_TAB, value)

    def get_clearing_account_type_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.CLEARING_ACCOUNT_TYPE_AT_VALUES_TAB)

    def set_client_id_source_at_values_tab(self, value):
        self.set_combobox_value(WashBookConstants.CLIENT_ID_SOURCE_AT_VALUES_TAB, value)

    def get_client_id_source_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.CLIENT_ID_SOURCE_AT_VALUES_TAB)

    def set_counterpart_at_values_tab(self, value):
        self.set_combobox_value(WashBookConstants.COUNTERPART_AT_VALUES_TAB, value)

    def get_counterpart_at_values_tab(self):
        return self.get_text_by_xpath(WashBookConstants.COUNTERPART_AT_VALUES_TAB)

    # click on
    def click_on_save_changes(self):
        self.find_by_xpath(WashBookConstants.SAVE_CHANGES_AT_WIZARD).click()

    # endregion
