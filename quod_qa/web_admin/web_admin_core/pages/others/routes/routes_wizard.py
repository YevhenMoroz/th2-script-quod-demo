from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_constants import RoutesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RoutesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_revert_changes(self):
        self.find_by_xpath(RoutesConstants.REVERT_CHANGES_AT_VALUES_TAB_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(RoutesConstants.SAVE_CHANGES_AT_VALUES_TAB_XPATH).click()

    def click_on_close_page_button(self):
        self.find_by_xpath(RoutesConstants.CLOSE_PAGE_AT_ROUTES_WIZARD).click()

    def click_on_download_pdf(self):
        self.find_by_xpath(RoutesConstants.DOWNLOAD_PDF_AT_ROUTES_WIZARD).click()

    # ==VALUES TAB==
    # setters
    def set_name_at_values_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.NAME_AT_VALUES_TAB_XPATH, value)

    def set_client_id_at_values_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.CLIENT_ID_AT_VALUES_TAB_XPATH, value)

    def set_es_instance_at_values_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.ES_INSTANCE_AT_VALUES_TAB_XPATH, value)

    def set_description_at_values_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.DESCRIPTION_AT_VALUES_TAB_XPATH, value)

    def set_counterpart_at_values_tab(self, value):
        self.set_combobox_value(RoutesConstants.COUNTERPART_AT_VALUES_TAB_XPATH, value)

    def set_support_contra_firm_commission_checkbox_at_values_tab(self):
        self.find_by_xpath(RoutesConstants.SUPPORT_CONTRA_FIRM_COMMISSION_AT_VALUES_TAB_XPATH).click()

    # click on
    def click_on_manage_button_at_values_tab(self):
        self.find_by_xpath(RoutesConstants.MANAGE_AT_VALUES_TAB_XPATH).click()

    # getters
    def get_name_value_at_values_tab(self):
        return self.get_text_by_xpath(RoutesConstants.NAME_AT_VALUES_TAB_XPATH)

    def get_client_id_value_at_values_tab(self):
        return self.get_text_by_xpath(RoutesConstants.CLIENT_ID_AT_VALUES_TAB_XPATH)

    def get_es_instance_value_at_values_tab(self):
        return self.get_text_by_xpath(RoutesConstants.ES_INSTANCE_AT_VALUES_TAB_XPATH)

    def get_description_value_at_values_tab(self):
        return self.get_text_by_xpath(RoutesConstants.DESCRIPTION_AT_VALUES_TAB_XPATH)

    def get_counterpart_value_at_values_tab(self):
        return self.get_text_by_xpath(RoutesConstants.COUNTERPART_AT_VALUES_TAB_XPATH)

    def get_support_contra_firm_commission_checkbox_value_at_values_tab(self):
        return self.is_checkbox_selected(RoutesConstants.SUPPORT_CONTRA_FIRM_COMMISSION_AT_VALUES_TAB_XPATH)

    def get_actual_error_after_click_on_next_in_empty_page(self):
        return self.find_by_xpath(RoutesConstants.EXPECTED_ERROR_FOR_VALUE_FIELD_AT_VALUES_TAB_XPATH).text
