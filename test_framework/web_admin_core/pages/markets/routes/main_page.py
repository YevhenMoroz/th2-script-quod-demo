import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.routes.constants import RoutesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class RoutesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_new_button(self):
        self.find_by_xpath(RoutesConstants.NEW_BUTTON_XPATH).click()

    def click_on_refresh_page_button(self):
        self.find_by_xpath(RoutesConstants.REFRESH_PAGE_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(RoutesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(RoutesConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(RoutesConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_on_delete_at_more_actions(self):
        self.find_by_xpath(RoutesConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(RoutesConstants.DOWNLOAD_PDF_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_action(self):
        self.find_by_xpath(RoutesConstants.PIN_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_ok(self):
        self.find_by_xpath(RoutesConstants.OK_BUTTON_AT_MORE_ACTIONS_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(RoutesConstants.CANCEL_BUTTON_AT_MORE_ACTIONS_XPATH).click()

    # --Filter Setters--
    def set_name_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.NAME_FILTER_XPATH, value)

    def set_description_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.DESCRIPTION_FILTER_XPATH, value)

    def set_es_instance_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.ES_INSTANCE_FILTER_XPATH, value)

    def set_client_id_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.CLIENT_ID_FILTER_XPATH, value)

    def set_default_strategy_type_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.DEFAULT_STRATEGY_TYPE_FILTER_XPATH, value)

    def set_counterpart_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.COUNTERPART_FILTER_XPATH, value)

    def set_support_contra_firm_commission_at_filter(self, value):
        self.set_text_by_xpath(RoutesConstants.SUPPORT_CONTRA_FIRM_COMMISSION_FILTER_XPATH, value)

    # --Filter getters--
    def get_name_value(self):
        return self.find_by_xpath(RoutesConstants.NAME_VALUE_XPATH).text

    def get_description_value(self):
        return self.find_by_xpath(RoutesConstants.DESCRIPTION_VALUE_XPATH).text

    def get_es_instance_value(self):
        return self.find_by_xpath(RoutesConstants.ES_INSTANCE_VALUE_XPATH).text

    def get_client_id_value(self):
        return self.find_by_xpath(RoutesConstants.CLIENT_ID_VALUE_XPATH).text

    def get_default_strategy_type_value(self):
        return self.find_by_xpath(RoutesConstants.DEFAULT_STRATEGY_TYPE_VALUE_XPATH).text

    def get_counterpart_value(self):
        return self.find_by_xpath(RoutesConstants.COUNTERPART_VALUE_XPATH).text

    def get_support_contra_firm_commission_value(self):
        return self.find_by_xpath(RoutesConstants.SUPPORT_CONTRA_FIRM_COMMISSION_VALUE_XPATH).text

    def is_searched_route_found(self, value):
        return self.is_element_present(RoutesConstants.DISPLAYED_ROUTE_XPATH.format(value))
