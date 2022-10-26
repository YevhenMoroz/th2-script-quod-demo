from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesRoutingParamGroupsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_DELETE_BUTTON_XPATH).click()

    def click_on_entity_at_routing_param_groups(self):
        self.find_by_xpath(VenuesConstants.CREATED_NAME_ROUTING_PARAM_GROUPS_TAB_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(VenuesConstants.CREATED_NAME_ROUTING_PARAM_GROUPS_TAB_XPATH).text

    def set_name_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_NAME_FILTER_XPATH, value)

    def set_positive_routes(self, value):
        self.set_checkbox_list(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_POSITIVE_ROUTES_XPATH, value)

    def set_positive_routes_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_POSITIVE_ROUTES_FILTER_XPATH, value)

    def click_on_positive_rotes(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_POSITIVE_ROUTES_XPATH).click()

    def get_positive_routes(self):
        return self.find_by_xpath(VenuesConstants.CREATED_POSITIVE_ROUTES_ROUTING_PARAM_GROUPS_TAB_XPATH).text

    def set_negative_routes(self, value):
        self.set_checkbox_list(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_NEGATIVE_ROUTES_XPATH, value)

    def get_negative_routes(self):
        return self.find_by_xpath(VenuesConstants.CREATED_NEGATIVE_ROUTES_ROUTING_PARAM_GROUPS_TAB_XPATH).text

    def click_on_negative_routes(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_NEGATIVE_ROUTES_XPATH).click()

    def set_negative_routes_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAM_GROUPS_TAB_NEGATIVE_ROUTES_FILTER_XPATH, value)

    # --------------------Parameters---------
    def click_on_plus_button_at_parameters(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_parameters(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_parameters(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_parameters(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_parameters(self):
        self.find_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_PLUS_DELETE_BUTTON_XPATH).click()

    def set_parameter(self, value):
        self.set_combobox_value(VenuesConstants.ROUTING_PARAMETERS_TAB_PARAMETER_XPATH, value)

    def get_parameter(self):
        return self.find_by_xpath(VenuesConstants.CREATED_PARAMETER_ROUTING_PARAMETERS_TAB_XPATH).text

    def set_parameter_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_PARAMETER_FILTER_XPATH, value)

    def set_value(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_VALUE_XPATH, value)

    def get_value(self):
        return self.find_by_xpath(VenuesConstants.CREATED_VALUE_ROUTING_PARAM_GROUPS_TAB_XPATH).text

    def set_value_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.ROUTING_PARAMETERS_TAB_VALUE_FILTER_XPATH, value)
