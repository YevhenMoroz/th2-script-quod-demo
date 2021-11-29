from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.others.routes.routes_constants import RoutesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RoutesTypeTifSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_at_type_tif_wizard(self):
        self.find_by_xpath(RoutesConstants.PLUS_BUTTON_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).click()

    def click_on_checkmark_at_type_tif_wizard(self):
        self.find_by_xpath(RoutesConstants.CHECK_MARK_BUTTON_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).click()

    def click_on_close_at_type_tif_wizard(self):
        self.find_by_xpath(RoutesConstants.CLOSE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).click()

    def click_on_ok_at_type_tif_wizard(self):
        self.find_by_xpath(RoutesConstants.OK_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).click()

    # setters
    def set_time_in_force_at_type_tif_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.TIME_IN_FORCE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH, value)

    def set_ord_type_at_type_tif_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.ORD_TYPE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH, value)

    def set_support_display_quantity_checkbox_at_type_tif_wizard(self):
        self.find_by_xpath(
            RoutesConstants.SUPPORT_DISPLAY_QUANTITY_CHECKBOX_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).click()

    def set_time_in_force_filter_at_type_tif_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.TIME_IN_FORCE_FILTER_AT_MANAGE_TYPE_TIF_WIZARD_XPATH, value)

    def set_ord_type_filter_at_type_tif_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.ORD_TYPE_AT_FILTER_MANAGE_TYPE_TIF_WIZARD_XPATH, value)

    def set_support_display_quantity_filter_at_type_tif_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.SUPPORT_DISPLAY_QUANTITY_FILTER_AT_MANAGE_TYPE_TIF_WIZARD_XPATH,
                               value)

    # getters
    def get_time_in_force_value_at_type_tif_wizard(self):
        return self.find_by_xpath(RoutesConstants.TIME_IN_FORCE_VALUE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).text

    def get_ord_type_value_at_type_tif_wizard(self):
        return self.find_by_xpath(RoutesConstants.ORD_TYPE_VALUE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).text

    def get_support_display_quantity_value_at_type_tif_wizard(self):
        return self.find_by_xpath(
            RoutesConstants.SUPPORT_DISPLAY_QUANTITY_VALUE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH).text
